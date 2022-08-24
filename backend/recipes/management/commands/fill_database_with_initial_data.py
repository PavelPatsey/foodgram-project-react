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

        tag_breakfast = Tag.objects.create(
            name="Завтрак",
            color="#f44336",
            slug="breakfast",
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

        # Создание рецепта Завтрак Сэндвич "Крок Месье"
        with open("data/text_sandwich") as file:
            text_sandwich = file.read().strip()
        recipe_sandwich = Recipe.objects.create(
            author=author_lena,
            name="Завтрак Сэндвич \"Крок Месье\"",
            text=text_sandwich,
            cooking_time=60,
        )

        with open("data/sandwich_base64code") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="sandwich." + "png")
        recipe_sandwich.image = data
        recipe_sandwich.save()

        recipe_sandwich.tags.add(tag_breakfast)

        # Лимоны - 2 шт.
        ingredient_lemon, _ = Ingredient.objects.get_or_create(
            name="лимоны",
            measurement_unit="шт.",
        )
        ingredientamount_lemon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_lemon,
            amount=2,
        )
        # Хлеб (для тостов) — 8 шт
        ingredient_bread, _ = Ingredient.objects.get_or_create(
            name="хлеб (для тостов)",
            measurement_unit="шт.",
        )
        ingredientamount_bread, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_bread,
            amount=8,
        )
        # Ветчина (150 гр) — 4 шт
        ingredient_ham, _ = Ingredient.objects.get_or_create(
            name="ветчина",
            measurement_unit="г",
        )
        ingredientamount_ham, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_ham,
            amount=150,
        )
        # Сыр твердый (желательно эмменталь) — 90 г
        ingredient_cheese, _ = Ingredient.objects.get_or_create(
            name="сыр Эмменталь",
            measurement_unit="г",
        )
        ingredientamount_cheese, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cheese,
            amount=90,
        )
        # Молоко — 250 мл
        ingredient_milk, _ = Ingredient.objects.get_or_create(
            name="молоко",
            measurement_unit="мл",
        )
        ingredientamount_milk, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_milk,
            amount=250,
        )
        # Мука пшеничная / Мука — 1 ст. л.
        ingredient_flour, _ = Ingredient.objects.get_or_create(
            name="мука пшеничная",
            measurement_unit="ст. л.",
        )
        ingredientamount_flour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_flour,
            amount=1,
        )
        # Масло сливочное — 20 г
        ingredient_butter, _ = Ingredient.objects.get_or_create(
            name="масло сливочное",
            measurement_unit="г",
        )
        ingredientamount_butter, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_butter,
            amount=20,
        )
        # соль - по вкусу
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="по вкусу",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # перец - по вкусу)
        ingredient_pepper, _ = Ingredient.objects.get_or_create(
            name="перец",
            measurement_unit="по вкусу",
        )
        ingredientamount_pepper, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_pepper,
            amount=1,
        )
        # Орех мускатный (на кончике ножа)
        ingredient_nutmeg, _ = Ingredient.objects.get_or_create(
            name="орех мускатный",
            measurement_unit="на кончике ножа",
        )
        ingredientamount_nutmeg, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_nutmeg,
            amount=1,
        )
        recipe_sandwich.ingredients.add(
            ingredientamount_bread,
            ingredientamount_ham,
            ingredientamount_cheese,
            ingredientamount_milk,
            ingredientamount_flour,
            ingredientamount_salt,
            ingredientamount_pepper,
            ingredientamount_nutmeg,
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
            measurement_unit="мл",
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
