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

    def __str__(self):
        return self.slug[:15]


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

    def __str__(self):
        return self.name + ", " + str(self.measurement_unit)


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.IntegerField(verbose_name="Количество")

    def __str__(self):
        return str(self.ingredient) + " * " + str(self.amount)


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Список тегов",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
    )
    ingredients = models.ManyToManyField(
        IngredientAmount,
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

    def __str__(self):
        return str(self.author) + ", " + str(self.name)


