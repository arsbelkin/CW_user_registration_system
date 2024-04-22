from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import City


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "username",
                "placeholder": "Username",
                "name": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "Password",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        error_messages={"unique": "Пользователь с таким логином уже существует"},
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "username",
                "placeholder": "Username",
                "name": "username",
            }
        ),
    )

    email = forms.CharField(
        label="email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "floatingEmail",
                "type": "email",
                "placeholder": "Email",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "Password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "Repeat password",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают", code='password_mismatch')
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=data).exists():
            raise forms.ValidationError("Такой e-mail уже используется", code='unique')
        return data


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        error_messages={'unique': 'Пользователь с таким логином уже существует'},
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "username",
                "placeholder": "Username",
                "name": "username",
            }
        ),
    )

    email = forms.CharField(
        error_messages={'unique': 'Пользователь с таким e-mail уже существует'},
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingEmail",
                "type": "email",
                "placeholder": "Email",
            }
        ),
    )

    class CustomSelect(forms.Select):
        option_inherits_attrs = True

    gender = forms.ChoiceField(
        label='Пол',
        choices=(("", "Не указан"), ("m", "Мужчина"), ("f", "Женщина")),
        required=False,
        widget=CustomSelect(
            attrs={
                "class": "form-control text-center",
                "id": "inputState",
            }
        ),
    )

    last_name = forms.CharField(
        label="Фамилия",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Фамилия",
            }
        ),
    )

    first_name = forms.CharField(
        label="Имя",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Имя",
            }
        ),
    )

    patronymic = forms.CharField(
        label="Отчество",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Отчество",
            }
        ),
    )

    city = forms.ModelChoiceField(
        label='Город',
        queryset=City.objects.filter(is_available=True).order_by("name"),
        required=False,
        widget=CustomSelect(
            attrs={
                "class": "form-control text-center",
                "id": "inputState",
            }
        ),
    )

    date_of_birth = forms.DateField(
        label="Дата рождения",
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "form-control",
            },
        ),
        input_formats=["%Y-%m-%d"],
    )

    image = forms.FileField(
        label="image",
        required=False,
        widget=forms.FileInput(
            attrs={
                "type": "file",
                "id": "photoInput",
                "accept": "image/*",
                "class": "file-upload",
            }
        ),
    )

    is_displayed = forms.BooleanField(
        label="Отображать пользователя в списке пользователей",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "role": "switch",
                "id": "flexSwitchCheckDefault",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "gender",
            "city",
            "date_of_birth",
            "image",
            "is_displayed",
        ]


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "Old password",
            }
        ),
    )

    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "new password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "repeat password",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "old_password",
            "new_password1",
            "new_password2",
        ]


class AddCityForm(forms.ModelForm):
    name = forms.CharField(
        label="Название города",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "text",
                "placeholder": "city_name",
                "name": "city_name",
            }
        ),
    )

    class Meta:
        model = City
        fields = [
            "name",
        ]


class DeleteUserForm(forms.Form):
    confirmation = forms.CharField(
        label="Подтверждение",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingInput",
                "type": "text",
                "placeholder": "confirmation",
                "name": "confirmation",
            }
        ),
    )

    def clean_confirmation(self):
        confirmation = self.cleaned_data["confirmation"]
        hidden_data = self.data["hidden_data"]
        if not (confirmation == f"users/{hidden_data}"):
            raise forms.ValidationError(message="Введите правильный код подтверждения")


class PasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "floatingEmail",
                "type": "email",
                "placeholder": "Email",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
        ]


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="new password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "new password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="repeat new password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "floatingPassword",
                "type": "password",
                "placeholder": "repeat password",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "new_password1",
            "new_password2",
        ]
