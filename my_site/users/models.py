from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from datetime import date
from django.urls import reverse


# Create your models here.
class City(models.Model):
    name = models.CharField(
        max_length=25, unique=True, db_index=True, verbose_name="Название"
    )

    is_available = models.BooleanField(default=False, verbose_name="Доступен для выбора")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "cities"


def user_directory_path(instance, filename):
    return "users/user_{0}/{1}".format(instance.id, filename)


@deconstructible
class TodayDateValidator:
    code = "today_date"

    def __init__(self, message=None):
        self.message = message if message else "Дата рождения не может быть в будущем"

    def __call__(self, value, *args, **kwds):
        data = str(value).split("-")
        today = str(date.today()).split("-")

        if not all(((int(data[i]) <= int(today[i])) for i in range(3))):
            raise ValidationError(self.message, code=self.code)


class User(AbstractUser):
    GENDERS = (("m", "Мужчина"), ("f", "Женщина"))

    email = models.EmailField(
        verbose_name='e-mail', blank=False, unique=True
    )

    patronymic = models.CharField(
        verbose_name="Отчество", blank=True, null=True, max_length=50, default=""
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True,
        validators=[
            TodayDateValidator(),
        ],
    )
    city = models.ForeignKey(to=City, null=True, on_delete=models.SET_NULL, blank=True)
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        blank=True,
        null=True,
        choices=GENDERS,
        default="",
    )
    image = models.ImageField(
        upload_to=user_directory_path, verbose_name="Фотография", blank=True, null=True
    )
    is_displayed = models.BooleanField(verbose_name="Отображается в списке", default=False)

    def get_absolute_url(self):
        return reverse('users:show_user', kwargs={'username': self.username})
    