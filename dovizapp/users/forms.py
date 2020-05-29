from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import DumanUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = DumanUser
        fields = ('email', 'phone_number', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = DumanUser
        fields = ('email', 'phone_number', 'password')