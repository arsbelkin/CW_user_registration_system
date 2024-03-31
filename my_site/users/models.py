from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25, db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class User(AbstractUser):
    GENDERS = (("m", "Мужчина"), ("f", "Женщина"))

    patronymic = models.CharField(
        verbose_name="Отчество", blank=True, null=True, max_length=50, default=""
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения", default="2005-01-01")
    city = models.ForeignKey(to=City, null=True, on_delete=models.SET_NULL)
    gender = models.CharField(
        verbose_name="Пол",
        max_length=1,
        blank=True,
        null=True,
        choices=GENDERS,
        default="",
    )
    image = models.ImageField(upload_to="users", verbose_name="Фотография")
