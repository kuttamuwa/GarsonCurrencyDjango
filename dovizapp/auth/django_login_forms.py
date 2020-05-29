from django import forms


class UserPassLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Kullanıcı Adı',
        max_length=20
    )
    password = forms.CharField(
        required=True,
        label='Şifre',
        max_length=32,
        widget=forms.PasswordInput()
    )


class PhoneLoginForm(forms.Form):
    phone_sms_code = forms.IntegerField()


def seperate_forms(form):
    if form.is_valid():
        if form.cleaned_data.get('username'):
            return form, UserPassLoginForm

        elif form.cleaned_data.get('phone_sms_code'):
            return form, PhoneLoginForm

        else:
            raise ModuleNotFoundError("Hatali form gonderildi?")
