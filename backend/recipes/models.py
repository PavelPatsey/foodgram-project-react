from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цветовой HEX-код",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
    )
