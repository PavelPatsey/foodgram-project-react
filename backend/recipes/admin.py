from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ("name", "author", "tags")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
