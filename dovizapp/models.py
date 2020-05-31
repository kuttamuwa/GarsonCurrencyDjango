from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class DumanUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None):
        if not email:
            raise ValueError('Kullanıcının geçerli bir mail adresine sahip olması gerekir !')
        if not username:
            raise ValueError('Kullanıcı adı girilmelidir')
        if not phone_number:
            raise ValueError('Telefon numarası girilmelidir')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone_number=phone_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class DumanUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'password', 'phone_number']

    objects = DumanUserManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
