from django.db import models
from django.contrib.auth.models import User, AbstractUser


class DumanUser(models.Model):
    phone_number = models.CharField(max_length=13)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# class NormalUser(AbstractUser):
#     pass

