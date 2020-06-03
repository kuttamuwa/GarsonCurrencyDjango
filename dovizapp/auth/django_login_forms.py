from django import forms


class UserPassLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Kullanıcı email',
        max_length=40
    )
    password = forms.CharField(
        required=False,
        label='Şifre',
        max_length=32,
        widget=forms.PasswordInput()
    )

    phone_sms_code = forms.CharField(
        required=False,
        label='Telefon doğrulama kodu',
        widget=forms.PasswordInput()
    )


