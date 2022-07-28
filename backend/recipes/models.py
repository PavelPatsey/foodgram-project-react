from django.db import models


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


class Ingredient(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=7,
        verbose_name="Цвет в HEX",
    )

    class Meta:
        unique_together = (
            "name",
            "measurement_unit",
        )
