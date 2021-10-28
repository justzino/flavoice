from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.CustomUser)
class UserAdmin(UserAdmin):

    additional_fieldsets = (
        (
            "추가 프로필",
            {
                "fields": (
                    "phone_number",
                    "birthday",
                    "gender",
                )
            },
        ),
    )
    fieldsets = UserAdmin.fieldsets + additional_fieldsets
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
