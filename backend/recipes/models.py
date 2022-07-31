from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет в HEX",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Уникальный слаг",
    )

    class Meta:
        unique_together = (
            "name",
            "color",
        )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=120,
        verbose_name="Цвет в HEX",
    )

    class Meta:
        unique_together = (
            "name",
            "measurement_unit",
        )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.ImageField(verbose_name="Количество")


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Список тегов",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
    )
    ingredients = models.ManyToManyField(
        IngredientAmount,
        on_delete=models.CASCADE,
        verbose_name="Список ингредиентов",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="media/recipes/images/",
        verbose_name="Картинка",
    )
    text = models.TextField(verbose_name="Описание")
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления (в минутах)",
    )


user = models.ForeignKey(
    User,
    models.SET_NULL,
    blank=True,
    null=True,
)
