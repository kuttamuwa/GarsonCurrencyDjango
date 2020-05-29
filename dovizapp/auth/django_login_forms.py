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

    phone_sms_code = forms.CharField(
        required=True,
        label='Telefon doğrulama kodu',
        widget=forms.PasswordInput()
    )


