import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from dovizapp.auth.auth_web import AuthPhone
from dovizapp.auth.django_login_forms import UserPassLoginForm
from dovizapp.forms import FormManager
from dovizapp.models import CustomUser
from dovizapp.pull_data.get_currency import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo


# Session.objects.all().delete().   to clear session to reauth
def index(request):
    return render(request, 'site_pages/homepage.html')


def about_page(request):
    return render(request, 'site_pages/about.html')


def contact_page(request):
    return render(request, 'site_pages/contact.html')


def home_page(request):
    return render(request, 'site_pages/homepage.html')


def show_enduser_sarrafiye(request):
    kgrtry_value = MoneyData().runforsarrafiye()
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()
    sarrafiye_data = SarrafiyeInfo.order_sarrafiye(sarrafiye_data)

    # formatting currency
    sarrafiye_data = SarrafiyeInfo.format_currency_data(sarrafiye_data)

    return render(request, 'show_pages/web/web_sarrafiye.html', {'data': sarrafiye_data,
                                                                 'tarih': SarrafiyeInfo.get_tarih()})


def show_mobil_sarrafiye(request):
    get_money = MoneyData()
    kgrtry_value = get_money.runforsarrafiye()
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()
    sarrafiye_data = SarrafiyeInfo.order_sarrafiye(sarrafiye_data)

    # formatting currency
    sarrafiye_data = SarrafiyeInfo.format_currency_data(sarrafiye_data)
    tarih = get_money.get_tarih()

    return JsonResponse({'data': sarrafiye_data, 'tarih': tarih})


def show_mobil_kurlar(request):
    """
    Mobil uygulamanin bakacagi json dondurulen yer. Admin panelinde seçilenler dondurulur.
    :return:
    """
    get_data = MoneyData()
    data = get_data.runforme()
    data = [i for i in data if i.get('title') in MoneyData.get_para_birimleri_on()]
    data = get_data.order_money(data)

    # formatting currency
    data = MoneyData.format_currency_data(data)
    tarih = get_data.get_tarih()

    return JsonResponse(data={'data': data, 'tarih': tarih})


def show_enduser_kurlar(request):
    """
    Son kullanıcının webten bakacagi yer. Admin panelinde seçilenler dondurulur.
    :return:
    """
    # money
    get_data = MoneyData()
    money_data = get_data.runforme()
    money_data = MoneyData.add_data_state_info(money_data)
    money_data = MoneyData.add_data_makas_value_info(money_data)
    money_data = get_data.order_money(money_data)
    money_data = get_data.format_currency_data(money_data)

    data = [i for i in money_data if i['title'] in MoneyData.get_para_birimleri_on()]
    tarih = get_data.get_tarih()

    return render(request, 'show_pages/web/web_kurlar.html', {'data': data, 'tarih': tarih})


def doviz_admin_login(request):
    if request.method == "GET":
        print("İlk form gönderildi, GET")
        # login sayfasi ilk açıldığında kullanıcı adı ve şifre girilir
        context = {'form': UserPassLoginForm}
        return render(request, 'authpages/gunes_first_auth.html', context)

    elif request.method == "POST":
        print("İkinci form gönderildi, POST. Ama hangisi bilmiyoruz")
        # form gönderilmiş, user-pwd mi yoksa tel kodu mu henüz bilmiyoruz
        form = UserPassLoginForm(request.POST)

        if form.is_valid():
            print("form geçerli")
            email = form.cleaned_data.get('email')

            if form.cleaned_data.get('phone_sms_code') == "":
                print("kullanıcı adı ve şifre gönderildi")
                # kullanıcı adı şifre girilmiş şimdi telefon kodu yollayacağız
                password = form.cleaned_data.get('password')
                try:
                    duman_user = authenticate(request, email=email, password=password)
                    print("authenticate fonksiyonu çalıştı")
                    if duman_user:
                        print("authenticate passed")
                        context = {'form': form, 'email': email}

                        # sms kodu yolla
                        sms_code = random.randint(10000, 99999)
                        phone_number = duman_user.phone_number
                        AuthPhone.set_sifre(phone_number, sms_code, duman_user)
                        print(f"sms code was set : {sms_code}")
                        if AuthPhone.send_msg(phone_number):
                            print("TELEFON NO HTML GONDERILECEK")
                            return render(request, 'authpages/gunes_phone_auth.html', context)

                        else:
                            print("Telefon no kod gönderilemedi")
                            return HttpResponse(ValueError('Telefon numarasına kod gönderilemedi'))
                    else:
                        print("Yanlis parola !")
                        return render(request, 'error_pages/wrong_password.html')

                except CustomUser.DoesNotExist:
                    print("User bulunamadı")
                    return render(request, 'error_pages/doesnotexist_user.html')

            else:
                try:
                    print("Telefon kodu gönderildi")
                    # sms kodu doğrulama
                    sent_sms_code = int(form.cleaned_data.get('phone_sms_code'))
                    phone_number = CustomUser.objects.get(email=email).phone_number
                    stored_sms_code = AuthPhone.get_sifre(phone_number)
                    print("Auth phone was gotten")
                    if stored_sms_code:
                        print("stored sms code was taken")
                        stored_sms_code, duman_user = stored_sms_code
                        if stored_sms_code == sent_sms_code:
                            print("Stored sms code equals sent sms code")
                            login(request, duman_user)
                            print("logged in")
                            AuthPhone.reset(phone_number)
                            return redirect('dovizadmin')

                        else:
                            print("wrong sms code")
                            return render(request, 'error_pages/wrong_sms_code.html')

                    else:
                        # demek ki email password kismi geçilmemiş bi şekilde direk kod denemesi yapilyor
                        print("imkansız nokta")
                        return render(request, 'error_pages/general_error.html',
                                      {
                                          'errors': 'Kullanıcı adı şifre girişi yapılmadan '
                                                    'telefon kodu şifresi denemesi yapiliyor!'})

                except CustomUser.DoesNotExist:
                    print("wrong sms code html rendered")
                    return render(request, 'error_pages/wrong_sms_code.html')

        else:
            print(f"general error form :{form.errors}")
            return render(request, 'error_pages/general_error.html', context={'errors': form.errors})


def dovizadmin_logout(request):
    logout(request)
    return redirect('homepage')


@login_required(login_url='login')
def manage_data_view(request):
    if request.method == 'POST':
        form_type = FormManager.return_form_one(request)
        if form_type == 1:
            # sarrafiyeadminform
            FormManager.sarrafiye_admin_manage(request.POST)
        elif form_type == 2:
            # moneyadminform
            FormManager.money_admin_manage(request.POST)

    elif request.method == 'GET':
        pass

    return load_admin_page(request)


def load_admin_page(request):
    # money
    get_data = MoneyData()
    money_data = get_data.runforme()
    money_data = MoneyData.add_data_state_info(money_data)
    money_data = MoneyData.add_data_makas_value_info(money_data)
    money_data = get_data.order_money(money_data)
    money_data = get_data.format_currency_data(money_data)

    # sarrafiye
    kgrtry_value = [i for i in money_data if i['title'] == "KGRTRY"][0]
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()
    sarrafiye_data = SarrafiyeInfo.add_data_state_info(sarrafiye_data)
    sarrafiye_data = SarrafiyeInfo.add_data_makas_value_info(sarrafiye_data)
    sarrafiye_data = SarrafiyeInfo.format_currency_data(sarrafiye_data)

    return render(request, 'admin_pages/data_managing_page.html', {
        'moneyshown': [i for i in money_data if i['title'] in MoneyData.get_para_birimleri_on()],
        'moneyadmin': money_data,
        'sarrafiyeshown': [i for i in sarrafiye_data if i['title'] in SarrafiyeInfo.get_on_represent_values()],
        'sarrafiyeadmin': sarrafiye_data,
        'tarih': get_data.get_tarih(),
        'email': 'admin'
    })
