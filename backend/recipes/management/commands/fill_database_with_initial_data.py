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
        tag_dessert = Tag.objects.create(
            name="Десерты",
            color="#ffb1d9",
            slug="dessert",
        )
        tag_main_course = Tag.objects.create(
            name="Основные блюда",
            # color="#bf9000",
            color="#bc4105",
            slug="main_course",
        )
        tag_soup = Tag.objects.create(
            name="Супы",
            color="#800020",
            slug="soup",
        )
        tag_salad = Tag.objects.create(
            name="Салаты",
            color="#48a357",
            slug="salad",
        )
        tag_hot_snack = Tag.objects.create(
            name="Горячие закуски",
            color="#d24508",
            slug="hot_snack",
        )
        tag_cold_snacks = Tag.objects.create(
            name="Холодные закуски",
            color="#4e8bc0",
            slug="cold_snacks",
        )
        tag_breakfast = Tag.objects.create(
            name="Завтрак",
            color="#f44336",
            slug="breakfast",
        )

        # Создание рецепта Завтрак Сэндвич "Крок Месье"
        with open("data/text_sandwich") as file:
            text_sandwich = file.read().strip()
        recipe_sandwich = Recipe.objects.create(
            author=author_lena,
            name='Завтрак Сэндвич "Крок Месье"',
            text=text_sandwich,
            cooking_time=30,
        )

        with open("data/base64code_sandwich") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="sandwich." + "png")
        recipe_sandwich.image = data
        recipe_sandwich.save()

        recipe_sandwich.tags.add(tag_breakfast)

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

        # Создание рецепта Паста карбонара с беконом и сливками
        with open("data/text_carbonara") as file:
            text_carbonara = file.read().strip()
        recipe_carbonara = Recipe.objects.create(
            author=author_lena,
            name="Паста карбонара с беконом и сливками",
            text=text_carbonara,
            cooking_time=30,
        )

        with open("data/base64code_carbonara") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="sandwich." + "png")
        recipe_carbonara.image = data
        recipe_carbonara.save()

        recipe_carbonara.tags.add(tag_main_course)

        # Паста сухая - 100 г
        ingredient_paste, _ = Ingredient.objects.get_or_create(
            name="паста",
            measurement_unit="г",
        )
        ingredientamount_paste, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_paste,
            amount=100,
        )
        # Бекон или панчетта - 80-100 г
        ingredient_bacon, _ = Ingredient.objects.get_or_create(
            name="бекон",
            measurement_unit="г",
        )
        ingredientamount_bacon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_bacon,
            amount=100,
        )
        # Сыр пармезан - 50 г
        ingredient_parmesan, _ = Ingredient.objects.get_or_create(
            name="сыр пармезан",
            measurement_unit="г",
        )
        ingredientamount_parmesan, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_parmesan,
            amount=50,
        )
        # Сливки 10-20% - 130 г
        ingredient_cream, _ = Ingredient.objects.get_or_create(
            name="сливки 10-20%",
            measurement_unit="г",
        )
        ingredientamount_cream, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cream,
            amount=130,
        )
        # Яйцо - 1 шт.
        ingredient_egg, _ = Ingredient.objects.get_or_create(
            name="яйцо куриное",
            measurement_unit="шт.",
        )
        ingredientamount_egg, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_egg,
            amount=1,
        )
        # Перец черный
        ingredient_pepper, _ = Ingredient.objects.get_or_create(
            name="перец черный",
            measurement_unit="по вкусу",
        )
        ingredientamount_pepper, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_pepper,
            amount=1,
        )
        # Чеснок - по вкусу
        ingredient_garlic, _ = Ingredient.objects.get_or_create(
            name="чеснок",
            measurement_unit="по вкусу",
        )
        ingredientamount_garlic, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_garlic,
            amount=1,
        )
        recipe_carbonara.ingredients.add(
            ingredientamount_paste,
            ingredientamount_bacon,
            ingredientamount_parmesan,
            ingredientamount_cream,
            ingredientamount_egg,
            ingredientamount_pepper,
            ingredientamount_garlic,
        )

        # Создание рецепта выпечка Сливовый пирог
        with open("data/text_plum_cake") as file:
            text_plum_cake = file.read().strip()
        recipe_plum_cake = Recipe.objects.create(
            author=author_pavel,
            name="Сливовый пирог",
            text=text_plum_cake,
            cooking_time=60,
        )

        with open("data/base64code_plum_cake") as file:
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

        # Создание рецепта суп Борщ
        with open("data/text_borsch") as file:
            text_borsch = file.read().strip()
        recipe_borsch = Recipe.objects.create(
            author=author_pavel,
            name="Борщ",
            text=text_borsch,
            cooking_time=120,
        )

        with open("data/base64code_borsch") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="borsch." + "png")
        recipe_borsch.image = data
        recipe_borsch.save()

        recipe_borsch.tags.add(tag_soup)

        # Говядина - 500 г
        ingredient_beef, _ = Ingredient.objects.get_or_create(
            name="говядина",
            measurement_unit="г",
        )
        ingredientamount_beef, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_beef,
            amount=500,
        )
        # Свёкла - 1 шт.
        ingredient_beet, _ = Ingredient.objects.get_or_create(
            name="свекла",
            measurement_unit="шт.",
        )
        ingredientamount_beet, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_beet,
            amount=1,
        )
        # Картофель - 2 шт.
        ingredient_potato, _ = Ingredient.objects.get_or_create(
            name="картофель",
            measurement_unit="шт.",
        )
        ingredientamount_potato, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_potato,
            amount=1,
        )
        # Капуста белокочанная - 200 г
        ingredient_cabbage, _ = Ingredient.objects.get_or_create(
            name="капуста белокочанная",
            measurement_unit="г",
        )
        ingredientamount_cabbage, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cabbage,
            amount=200,
        )
        # Морковь - 1 шт.
        ingredient_carrot, _ = Ingredient.objects.get_or_create(
            name="морковь",
            measurement_unit="шт.",
        )
        ingredientamount_carrot, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_carrot,
            amount=1,
        )
        # Лук репчатый - 1 шт.
        ingredient_onion, _ = Ingredient.objects.get_or_create(
            name="лук репчатый",
            measurement_unit="шт.",
        )
        ingredientamount_onion, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_onion,
            amount=1,
        )
        # Томатная паста - 1 ст. ложка
        ingredient_tomato, _ = Ingredient.objects.get_or_create(
            name="томатная паста",
            measurement_unit="ст. ложка",
        )
        ingredientamount_tomato, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_tomato,
            amount=1,
        )
        # Масло растительное - 2 ст. ложки
        ingredient_oil, _ = Ingredient.objects.get_or_create(
            name="масло растительное",
            measurement_unit="ст. ложка",
        )
        ingredientamount_oil, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_oil,
            amount=2,
        )
        # Уксус - 1 ч. ложка
        ingredient_vinegar, _ = Ingredient.objects.get_or_create(
            name="уксус",
            measurement_unit="ч. ложка",
        )
        ingredientamount_vinegar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_vinegar,
            amount=1,
        )
        # Лавровый лист - 1 шт.
        ingredient_laurel, _ = Ingredient.objects.get_or_create(
            name="лавровый лист",
            measurement_unit="шт.",
        )
        ingredientamount_laurel, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_laurel,
            amount=1,
        )
        # Перец чёрный горошком - 2-3 шт.
        ingredient_peppercorns, _ = Ingredient.objects.get_or_create(
            name="перец чёрный горошком",
            measurement_unit="шт.",
        )
        (
            ingredientamount_peppercorns,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_peppercorns,
            amount=3,
        )
        # Соль - 2 ч. ложки (по вкусу)
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="по вкусу",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # Вода - 1,5 л
        ingredient_water, _ = Ingredient.objects.get_or_create(
            name="вода",
            measurement_unit="мл",
        )
        ingredientamount_water, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_water,
            amount=1500,
        )
        # Зелень укропа и/или петрушки (для подачи) - 3-4 веточки
        ingredient_dill, _ = Ingredient.objects.get_or_create(
            name="зелень укропа",
            measurement_unit="веточка",
        )
        ingredientamount_dill, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_dill,
            amount=1,
        )
        # Зелень укропа и/или петрушки (для подачи) - 3-4 веточки
        ingredient_parsley, _ = Ingredient.objects.get_or_create(
            name="зелень петрушки",
            measurement_unit="веточка",
        )
        ingredientamount_parsley, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_parsley,
            amount=1,
        )
        # Сметана (для подачи) - 2 ст. ложки
        ingredient_sour, _ = Ingredient.objects.get_or_create(
            name="сметана",
            measurement_unit="ст. ложка",
        )
        ingredientamount_sour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sour,
            amount=2,
        )
        recipe_borsch.ingredients.add(
            ingredientamount_beef,
            ingredientamount_beet,
            ingredientamount_potato,
            ingredientamount_cabbage,
            ingredientamount_carrot,
            ingredientamount_onion,
            ingredientamount_tomato,
            ingredientamount_oil,
            ingredientamount_vinegar,
            ingredientamount_laurel,
            ingredientamount_peppercorns,
            ingredientamount_salt,
            ingredientamount_water,
            ingredientamount_dill,
            ingredientamount_parsley,
            ingredientamount_sour,
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

        with open("data/base64code_lemonade") as file:
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
