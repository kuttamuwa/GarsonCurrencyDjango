# from dovizapp.models import DBConnection

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from dovizapp.pull_data.get_currency import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'phone_number')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number')


class FormManager:
    # kolay olsun diye
    formtypes = {'sarrafiyeadminform': 1, 'moneyadminform': 2}
    # _dbconnection = DBConnection.get_db_connection()

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

        # df = pd.DataFrame.from_dict(sarrafiye_form)
        # df.to_sql('sarrafiye_makas_table', con=FormManager._dbconnection, if_exists='replace')

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
