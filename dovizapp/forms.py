from django.contrib.auth.forms import UserCreationForm

from dovizapp.models import DumanUser
from dovizapp.pull_data.get_and_save import MoneyData
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
        # todo : iki ayrı form tasarlanacak
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

        for i in sarrafiye_form.items():

            if i not in ('sarrafiyeadminform', 'csrfmiddlewaretoken'):
                key, value = i
                if str(key).count('?'):
                    # artis azalis degerleri gelir
                    term, sarrafiye = key.split('?')
                    if value != "":  # isaretlendi ama deger girilmemis olabilir?
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
            if row[0].count("?"):
                # makas degerleri
                term, currency = row[0].split("?")
                if term == 'artis':
                    if row[1] != "":  # isaretlendi ama deger girilmemis olabilir?
                        MoneyData.set_makas_artis_value(currency, row[1][1])
                elif term == 'azalis':
                    if row[1] != "":  # isaretlendi ama deger girilmemis olabilir?
                        MoneyData.set_makas_azalis_value(currency, row[1][1])

            else:
                if row[1] == 'on':  # checkbox isaretlendiyse
                    MoneyData.set_para_birimi_on(row[0])
