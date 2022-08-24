import base64
import csv

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import User


class Command(BaseCommand):
    help = "Fill the database with initial data"

    def handle(self, *args, **kwargs):
        with open("data/ingredients.csv", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )

        author_pavel = User.objects.create(
            username="pavelpatsey",
            first_name="Павел",
            last_name="Пацей",
            email="pavelpatsey@mail.ru",
        )
        author_lena = User.objects.create(
            username="lenaarhipova",
            first_name="Лена",
            last_name="Архипова",
            email="lenaarhipova@mail.ru",
        )

        tag_drinks = Tag.objects.create(
            name="Напитки",
            color="#c69d21",
            slug="drinks",
        )
        tag_baked_goods = Tag.objects.create(
            name="Выпечка",
            color="#874e24",
            slug="baked_goods",
        )

        # Создание рецепта напитки Лимонад
        with open("data/text_lemonade") as file:
            text_lemonade = file.read().strip()
        recipe_lemonade = Recipe.objects.create(
            author=author_pavel,
            name="Освежающий лимонад",
            text=text_lemonade,
            cooking_time=60,
        )

        with open("data/lemonade_base64code") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="lemonade." + "png")
        recipe_lemonade.image = data
        recipe_lemonade.save()

        recipe_lemonade.tags.add(tag_drinks)

        # Лимоны - 2 шт.
        ingredient_lemon, _ = Ingredient.objects.get_or_create(
            name="лимоны",
            measurement_unit="шт.",
        )
        ingredientamount_lemon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_lemon,
            amount=2,
        )
        # Мята перечная свежая - 6 веточек
        ingredient_peppermint, _ = Ingredient.objects.get_or_create(
            name="мята перечная свежая",
            measurement_unit="веточка",
        )
        (
            ingredientamount_peppermint,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_peppermint,
            amount=6,
        )
        # Сахар - 125 г
        ingredient_sugar, _ = Ingredient.objects.get_or_create(
            name="сахар",
            measurement_unit="г",
        )
        ingredientamount_sugar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sugar,
            amount=125,
        )
        # Вода - 2,5 л
        ingredient_water, _ = Ingredient.objects.get_or_create(
            name="вода",
            measurement_unit="г",
        )
        ingredientamount_water, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_water,
            amount=2500,
        )
        recipe_lemonade.ingredients.add(
            ingredientamount_lemon,
            ingredientamount_peppermint,
            ingredientamount_sugar,
            ingredientamount_water,
        )

        # Создание рецепта выпечка Сливовый пирог
        with open("data/text_plum_cake") as file:
            text_plum_cake = file.read().strip()
        recipe_plum_cake = Recipe.objects.create(
            author=author_lena,
            name="Сливовый пирог",
            text=text_plum_cake,
            cooking_time=60,
        )

        with open("data/plum_cake_base64code") as file:
            imgstr = file.read().strip()
        data = ContentFile(
            base64.b64decode(imgstr), name="plum_cake." + "png"
        )
        recipe_plum_cake.image = data
        recipe_plum_cake.save()

        recipe_plum_cake.tags.add(tag_baked_goods)

        # Сливы - 12 шт.
        ingredient_plum, _ = Ingredient.objects.get_or_create(
            name="cлива",
            measurement_unit="шт.",
        )
        ingredientamount_plum, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_plum,
            amount=12,
        )
        # Сахар - 150 г
        ingredient_sugar, _ = Ingredient.objects.get_or_create(
            name="сахар",
            measurement_unit="г",
        )
        ingredientamount_sugar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sugar,
            amount=150,
        )
        # Соль - 1 щепотка
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="щепотка",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # Масло сливочное - 115 г
        ingredient_butter, _ = Ingredient.objects.get_or_create(
            name="масло сливочное",
            measurement_unit="г",
        )
        ingredientamount_butter, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_butter,
            amount=115,
        )
        # Мука - 120 г
        ingredient_flour, _ = Ingredient.objects.get_or_create(
            name="мука",
            measurement_unit="г",
        )
        ingredientamount_flour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_flour,
            amount=120,
        )
        # Яйца - 2 шт.
        ingredient_eggs, _ = Ingredient.objects.get_or_create(
            name="яйца куриные",
            measurement_unit="шт.",
        )
        ingredientamount_eggs, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_eggs,
            amount=2,
        )
        # Разрыхлитель - 1 ч. ложка
        ingredient_baking_powder, _ = Ingredient.objects.get_or_create(
            name="разрыхлитель",
            measurement_unit="ч. ложка",
        )
        (
            ingredientamount_baking_powder,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_baking_powder,
            amount=1,
        )
        # Корица молотая - 1 ч. ложка
        ingredient_cinnamon, _ = Ingredient.objects.get_or_create(
            name="корица молотая",
            measurement_unit="ч. ложка",
        )
        ingredientamount_cinnamon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cinnamon,
            amount=1,
        )
        recipe_plum_cake.ingredients.add(
            ingredientamount_plum,
            ingredientamount_sugar,
            ingredientamount_salt,
            ingredientamount_butter,
            ingredientamount_flour,
            ingredientamount_eggs,
            ingredientamount_baking_powder,
            ingredientamount_cinnamon,
        )
