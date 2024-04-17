from django.db.models.base import Model as Model
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, LoginUserForm, ProfileUserForm


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


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_photo'] = f"../../../media/{self.request.user.image}" if self.request.user.image != "" else None
        return context
