from django.contrib.auth.forms import UserCreationForm

from dovizapp.models import DumanUser


class DumanUserRegisterForm(UserCreationForm):
    class Meta:
        model = DumanUser
        fields = ['username', 'password1', 'password2', 'phone_number', 'email']


