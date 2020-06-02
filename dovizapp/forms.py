from django.contrib.auth.forms import UserCreationForm
from django import forms

from dovizapp.models import DumanUser
from dovizapp.pull_data.get_currency import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo


class DumanUserRegisterForm(UserCreationForm):
    class Meta:
        model = DumanUser
        fields = ['username', 'password1', 'password2', 'phone_number', 'email']


class FormManager:
    # kolay olsun diye
    formtypes = {'sarrafiyeadminform': 1, 'moneyadminform': 2}

    @classmethod
    def get_formtypes(cls, form_name):
        return cls.formtypes[form_name]

    @staticmethod
    def return_form_one(request):
        if [k for k, v in request.POST.items()].count('sarrafiyeadminform'):
            return FormManager.get_formtypes('sarrafiyeadminform')

        elif [k for k, v in request.POST.items()].count('moneyadminform'):
            return FormManager.get_formtypes('moneyadminform')

    @staticmethod
    def sarrafiye_admin_manage(sarrafiye_form):
        """

        :param sarrafiye_form:
        :return:
        """
        # tum checkboxlari kapatmis gibi gosterecegiz, cunku formda sadece acik emri bulunanlar geliyor.
        SarrafiyeInfo.turn_off_all_represent_values()

        for row in sarrafiye_form.items():

            if row not in ('sarrafiyeadminform', 'csrfmiddlewaretoken'):
                key, value = row
                if str(key).count('?'):
                    # artis azalis degerleri gelir
                    term, sarrafiye = key.split('?')
                    if value != "":
                        SarrafiyeInfo.set_makas_value(sarrafiye, value, term)

                else:
                    if value == 'on':
                        SarrafiyeInfo.turn_on_represent_value(key)

    @staticmethod
    def money_admin_manage(money_form):
        """

        :param money_form:
        :return:
        """
        MoneyData.set_para_birimleri_turn_off_all()

        for row in money_form.items():
            if row[0] not in ('moneyadminform', 'csrfmiddlewaretoken'):
                key, value = row
                if str(key).count("?"):
                    # makas degerleri
                    term, currency = key.split("?")
                    if term == 'artis':
                        if value != "":  # isaretlendi ama deger girilmemis olabilir?
                            MoneyData.set_makas_artis_value(currency, float(value))
                    elif term == 'azalis':
                        if value != "":  # isaretlendi ama deger girilmemis olabilir?
                            MoneyData.set_makas_azalis_value(currency, float(value))

                else:
                    if row[1] == 'on':  # checkbox isaretlendiyse
                        MoneyData.set_para_birimi_on(row[0])
