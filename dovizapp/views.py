from django.http import JsonResponse
from django.shortcuts import render

from dovizapp.pull_data.get_and_save import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo


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
