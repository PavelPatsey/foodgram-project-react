from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name="Название",
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цветовой HEX-код",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Slug",
    )

    # Название.
    # Цветовой HEX-код (например, #49B64E).
    # Slug.
