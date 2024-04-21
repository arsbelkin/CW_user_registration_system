from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "users"

urlpatterns = [
    # url-адреса входа и выхода
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # url-адреса смены пароля
    path(
        "password-change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # url-адреса сброса пароля
    path(
        "password-reset/", views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.ProfileUser.as_view(), name="profile"),
    path("add-city/", views.AddCityView.as_view(), name="add_city"),
    path("add-city/done", views.AddCityDoneView.as_view(), name="add_city_done"),
    path("delete-user/", views.DeleteUserView, name="delete_user"),
    path("list-of-users/", views.ListUserView.as_view(), name="list_of_users"),
    path("user/<slug:username>/", views.ShowUser.as_view(), name="show_user"),
]
