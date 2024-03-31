from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, City


# Register your models here.
admin.site.register(City)


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = ["id", "username", "email", "gender", "city", "is_staff"]
    list_display_links = ["id", "username"]
    list_filter = ["gender", "city", "is_staff"]

    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "patronymic",
                    ("date_of_birth", "gender", "city"),
                    "image",
                ]
            },
        ),
        ("Admin info", {"fields": ["is_superuser", "is_staff", "is_active"]}),
    ]

    add_fieldsets = [
        *UserAdmin.add_fieldsets,
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "patronymic",
                    ("date_of_birth", "gender", "city"),
                    "image",
                ]
            },
        ),
    ]
