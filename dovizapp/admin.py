from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.models import User

from dovizapp.models import DumanUser


class DumanUserInline(admin.StackedInline):
    model = DumanUser
    can_delete = True
    verbose_name_plural = 'dumanuser'


class DumanUserAdmin(BaseUserAdmin):
    inlines = (DumanUserInline, )


admin.site.unregister(User)
admin.site.register(DumanUser)
# admin.site.register(NormalUser, UserAdmin)
