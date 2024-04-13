from django.db.models.base import Model as Model
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, LoginUserForm, ProfileUserForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView


# Create your views here.
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "users/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "users/register.html", {"user_form": user_form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "registration/login.html"
