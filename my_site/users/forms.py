from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import City


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="username",
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
        label="password",
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
        label="username",
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
        label="password",
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
        label="repeat password",
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
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileUserForm(forms.ModelForm):
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

    class CustomSelect(forms.Select):
        option_inherits_attrs = True

    gender = forms.ChoiceField(
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
        label="last name",
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
        label="first name",
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
        label="patronymic",
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
        queryset=City.objects.order_by("name"),
        required=False,
        widget=CustomSelect(
            attrs={
                "class": "form-control text-center",
                "id": "inputState",
            }
        ),
    )

    date_of_birth = forms.DateField(
        label="Date of Birth",
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
        ]
