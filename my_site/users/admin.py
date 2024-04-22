from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import User, City


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "is_available",
    ]
    list_display_links = [
        "id",
        "name",
    ]
    actions = [
        "set_available",
        "set_unavailable",
    ]
    search_fields = ['name',]

    @admin.action(description="Сделать доступными")
    def set_available(self, request, queryset):
        count = queryset.update(is_available=True)
        self.message_user(request, f"{count} городов стали доступны")

    @admin.action(description="Ограничить доступ")
    def set_unavailable(self, request, queryset):
        count = queryset.update(is_available=False)
        self.message_user(
            request, f"{count} городов стали недоступны", messages.WARNING
        )


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = [
        "id",
        "username",
        "email",
        "gender",
        "city",
        "is_staff",
        "is_displayed",
    ]
    list_display_links = [
        "id",
        "username",
    ]
    list_filter = [
        "gender",
        "city",
        "is_staff",
        "is_displayed",
    ]

    fieldsets = [
        (None, {"fields": ["username", "password", "email"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "patronymic",
                    ("date_of_birth", "gender", "city"),
                    "image",
                    "is_displayed",
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
