from django.db.models.base import Model as Model
from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.contrib.auth import get_user_model, logout
from django.views.generic import (
    UpdateView,
    CreateView,
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import (
    UserRegistrationForm,
    LoginUserForm,
    ProfileUserForm,
    PasswordChangeForm,
    AddCityForm,
    DeleteUserForm,
    PasswordResetForm,
    PasswordResetConfirmForm,
)
from .models import City


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
    template_name = "users/profile.html"

    def get_success_url(self) -> str:
        return reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context

    def form_valid(self, form):
        if "checkbox" in form.data:
            instance = form.save(commit=False)
            instance.image = ""
            instance.save()
        return super(ProfileUser, self).form_valid(form)


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("users:password_change_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        logout(self.request)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context


class AddCityView(LoginRequiredMixin, CreateView):
    model = City
    form_class = AddCityForm
    template_name = "users/add_city.html"

    def get_success_url(self) -> str:
        return reverse_lazy("users:add_city_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context


class AddCityDoneView(LoginRequiredMixin, TemplateView):
    template_name = "users/add_city_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context


@login_required
def DeleteUserView(request):
    user_photo = (
        f"../../../media/{request.user.image}" if request.user.image != "" else None
    )
    if request.method == "POST":
        user_form = DeleteUserForm(request.POST)
        if user_form.is_valid():
            user = request.user
            request.session.flush()
            logout(request)
            get_user_model().objects.filter(id=user.id).delete()
            return render(request, "users/delete_user_done.html")
    else:
        user_form = DeleteUserForm()
    return render(
        request,
        "users/delete_user.html",
        {
            "form": user_form,
            "user_photo": user_photo,
        },
    )


class ListUserView(LoginRequiredMixin, ListView):
    template_name = "users/list_of_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return get_user_model().objects.filter(is_displayed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        return context


class ShowUser(DetailView):
    template_name = "users/detail_user.html"
    slug_url_kwarg = "username"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return get_user_model().objects.get(username=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        GENDERS = {"m": "Мужчина", "f": "Женщина"}

        context = super().get_context_data(**kwargs)
        context["user_photo"] = (
            f"../../../media/{self.request.user.image}"
            if self.request.user.image != ""
            else None
        )
        context["user_gender"] = GENDERS.get(context["user"].gender, "")
        return context


class PasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    form_class = PasswordResetForm

    def get_success_url(self) -> str:
        return reverse_lazy("users:password_reset_done")


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    form_class = PasswordResetConfirmForm

    def get_success_url(self) -> str:
        return reverse_lazy("users:password_reset_complete")
