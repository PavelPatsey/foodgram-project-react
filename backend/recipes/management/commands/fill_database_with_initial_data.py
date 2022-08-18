import csv

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
        # author_lena = User.objects.create(
        #     username="lenaarhipova",
        #     first_name="Лена",
        #     last_name="Архипова",
        #     email="lenaarhipova@mail.ru",
        # )

        tag_drinks = Tag.objects.create(
            name="Напитки",
            color="#0000ff",
            slug="drinks",
        )

        text_lemonade = (
            "Подготовить ингредиенты.\nВыдавить сок из лимонов."
            + " Положить в кастрюлю корки лимона, оборвать листики с мяты"
            + " и тоже положить в кастрюлю. Залить водой. Закипятить и варить"
            + " 3 минуты.\n"
            + "Добавить сахар, перемешать, выключить огонь. Оставить отвар до"
            + " полного остывания, затем процедить.\n"
            + "Добавить сок лимона и перемешать.\n"
            + "Охладить лимонад, разлить по стаканам, добавить лед. Украсить"
            + " освежающий лимонад листиками мяты.\nПриятного аппетита!"
        )
        recipe_lemonade = Recipe.objects.create(
            author=author_pavel,
            name="Освежающий лимонад",
            text=text_lemonade,
            cooking_time=60,
        )

        # recipe_lemonade.image = "data/image_lemonade.png"
        # recipe_lemonade.save()

        import base64

        from django.core.files.base import ContentFile

        with open("data/lemonade_base64code") as file:
            imgstr = file.read().strip()

        data = ContentFile(
            base64.b64decode(imgstr), name="temp." + "lemonade"
        )
        recipe_lemonade.image = data
        recipe_lemonade.save()
        # Test.objects.create(image=data)

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
