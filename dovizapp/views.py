import random

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import RequestContext

from dovizapp import Auth
from dovizapp.auth.auth_web import AuthPhone
from dovizapp.auth.django_login_forms import UserPassLoginForm, PhoneLoginForm, seperate_forms
from dovizapp.pull_data.get_and_save import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo

auth = Auth()
# Session.objects.all().delete().   to clear session to reauth

def index(request):
    return render(request, 'other_pages/homepage.html')


def about_page(request):
    return render(request, 'other_pages/about.html')


def contact_page(request):
    return render(request, 'other_pages/contact.html')


def home_page(request):
    return render(request, 'other_pages/homepage.html')


def show_enduser_sarrafiye(request):
    kgrtry_value = MoneyData().runforsarrafiye()
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()

    # formatting currency
    sarrafiye_data = SarrafiyeInfo.format_currency_data(sarrafiye_data)

    return render(request, 'sarrafiye.html', {'data': sarrafiye_data,
                                              'tarih': SarrafiyeInfo.get_tarih()})


def show_mobil_sarrafiye(request):
    get_money = MoneyData()
    kgrtry_value = get_money.runforsarrafiye()
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()

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


def username_password_form(request):
    if request.method == "POST":
        form = seperate_forms(request.POST)

        if isinstance(form, UserPassLoginForm):
            # verify and redirect to phone step
            username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
            verified = auth.verify_username_password(username, password)
            if verified:
                phone_number = auth.get_phone_number_username(username)

                sms_code = random.randint(10000, 99999)
                AuthPhone.set_sifre(phone_number, sms_code)
                # AuthPhone.send_msg(phone_number)
                return render(request, 'gunesadmin/gunes_phone_auth.html', {'form': PhoneLoginForm},
                              RequestContext(request))
            else:
                return HttpResponse("Verilen kullanıcı adı ve şifre yanlıştır !")

        elif isinstance(form, PhoneLoginForm):
            if AuthPhone.get_sifre(form.get('username')) == form.get('phone_sms_code'):

                return admin_page(request)

    elif request.method == "GET":
        return render(request, 'gunesadmin/gunes_first_auth.html', {'form': UserPassLoginForm},
                      RequestContext(request))


def show_enduser_kurlar(request):
    """
    Son kullanıcının webten bakacagi yer. Admin panelinde seçilenler dondurulur.
    :return:
    """
    get_data = MoneyData()
    data = get_data.runforme()
    data = [i for i in data if i.get('title') in MoneyData.get_para_birimleri_on()]
    data = get_data.order_money(data)
    tarih = get_data.get_tarih()

    # formatting currency
    data = MoneyData.format_currency_data(data)

    return render(request, 'kurlar.html', {'data': data, 'tarih': tarih})


def logout(request, username):
    print(f"{username} logged out")


@user_passes_test(lambda u: u.is_superuser)
def test_admin_page(request):
    return render(request, 'base.html')


@login_required
def admin_page(request):
    # money
    get_data = MoneyData()
    money_data = get_data.runforme()
    money_data = MoneyData.add_data_state_info(money_data)
    money_data = MoneyData.add_data_makas_value_info(money_data)

    # sarrafiye
    kgrtry_value = [i for i in money_data if i['title'] == "KGRTRY"][0]
    SarrafiyeInfo.set_kgrtry(kgrtry_value['alis'], kgrtry_value['satis'])
    sarrafiye_data = SarrafiyeInfo.get_data()
    sarrafiye_data = SarrafiyeInfo.add_data_state_info(sarrafiye_data)
    sarrafiye_data = SarrafiyeInfo.add_data_makas_value_info(sarrafiye_data)
    sarrafiye_data = SarrafiyeInfo.format_currency_data(sarrafiye_data)

    return render(request, 'onepage.html', {
        'moneyshown': [i for i in money_data if i['title'] in MoneyData.get_para_birimleri_on()],
        'moneyadmin': money_data,
        'sarrafiyeshown': [i for i in sarrafiye_data if i['title'] in SarrafiyeInfo.get_on_represent_values()],
        'sarrafiyeadmin': sarrafiye_data,
        'tarih': get_data.get_tarih(),
        'username': 'admin'
    })
