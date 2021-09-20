from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.CustomUser)
class UserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets
    list_display = UserAdmin.list_display
