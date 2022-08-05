import shutil
import tempfile
import unittest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from ..models import Ingredient, IngredientAmount, Recipe, Tag

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()
        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)
        cls.ingredient_1 = Ingredient.objects.create(
            name="test апельсин",
            measurement_unit="шт.",
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name="test варенье",
            measurement_unit="ложка",
        )
        cls.tag = Tag.objects.create(
            name="test Завтрак",
            color="#6AA84FFF",
            slug="breakfast",
        )
        cls.tag_2 = Tag.objects.create(
            name="test Обед",
            color="#6AA84FFF",
            slug="dinner",
        )
        cls.ingredientamount_1 = IngredientAmount.objects.create(
            ingredient=cls.ingredient_1,
            amount=5,
        )
        cls.ingredientamount_2 = IngredientAmount.objects.create(
            ingredient=cls.ingredient_2,
            amount=1,
        )
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded = SimpleUploadedFile(
            name="small.gif",
            content=cls.small_gif,
            content_type="image/gif",
        )
        cls.small_gif_1 = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded_1 = SimpleUploadedFile(
            name="small_1.gif",
            content=cls.small_gif_1,
            content_type="image/gif",
        )
        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name="test рецепт",
            image=cls.uploaded,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe.tags.add(cls.tag)
        cls.recipe.ingredients.add(
            cls.ingredientamount_1,
            cls.ingredientamount_2,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_recipes_list_unauthorized_user(self):
        """Получение списка рецептов неавторизованным пользователем"""
        url = "/api/recipes/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_recipes_list_authorized_client(self):
        """Получение списка рецептов авторизованным пользователем."""
        url = "/api/recipes/"
        recipe = Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            image=self.uploaded_1,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        recipe.tags.add(self.tag)
        recipe.ingredients.add(self.ingredientamount_1)
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        },
                        {
                            "id": 2,
                            "name": "test варенье",
                            "measurement_unit": "ложка",
                            "amount": 1,
                        },
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "test рецепт",
                    "image": "http://testserver/media/recipes/images/small.gif",
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 2,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        }
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "тестовый рецепт",
                    "image": "http://testserver/media/recipes/images/small_1.gif",
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_get_recipe_detail_unauthorized_client(self):
        """Получение рецепта неавторизованным пользователем."""
        url = f"/api/recipes/{self.user.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_get_recipe_detail_authorized_client(self):
        """Получение рецепта авторизованным пользователем."""
        url = f"/api/recipes/{self.user.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_unauthorized_client(self):
        """Создание рецепта неавторизованным пользователем."""
        url = "/api/recipes/"
        recipe_count = Recipe.objects.count()
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.guest_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Recipe.objects.count(), recipe_count)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_authorized_client(self):
        """Создание рецепта авторизованным пользователем."""
        url = "/api/recipes/"
        recipe_count = Recipe.objects.count()
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), recipe_count + 1)
        image = response.json().get("image")
        test_string = "http://testserver/media/recipes/images/"
        self.assertTrue(test_string in image)
        test_json = {
            "id": 2,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                },
                {
                    "id": 2,
                    "name": "test Обед",
                    "color": "#6AA84FFF",
                    "slug": "dinner",
                },
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 3,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 10,
                },
                {
                    "id": 4,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 30,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "Тестовый рецепт обеда",
            "image": image,
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_ingredients(self):
        """Создание рецепта.
        Игредиенты обязательное поле."""
        url = "/api/recipes/"
        data = {
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"ingredients": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_tags(self):
        """Создание рецепта.
        Теги обязательное поле."""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"tags": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_image(self):
        """Создание рецепта без рисунка."""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"image": ["Ни одного файла не было отправлено."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_name(self):
        """Создание рецепта.
        Название рецепта обязательное поле."""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"name": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_text(self):
        """Создание рецепта.
        Описание рецепта обязательное поле."""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"text": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_cooking_time(self):
        """Создание рецепта.
        Время готовки обязательное поле."""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"cooking_time": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_ingredients_tags(self):
        """Создание рецепта.
        Теги и игредиенты обязательные поля."""
        url = "/api/recipes/"
        data = {
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_with_empty_data(self):
        """Создание рецепта обязательные поля."""
        url = "/api/recipes/"
        data = {}
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
            "image": ["Ни одного файла не было отправлено."],
            "name": ["Обязательное поле."],
            "text": ["Обязательное поле."],
            "cooking_time": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_negative_cooking_time(self):
        """Создание рецепта авторизованным пользователем.
        с отрицательным временем готовки"""
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": -1,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "cooking_time": ["Убедитесь, что это значение больше либо равно 1."]
        }
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_authorized_client(self):
        """Обновление рецепта авторизованным пользователем."""
        recipe = Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            image=self.uploaded_1,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        recipe.tags.add(self.tag)
        recipe.ingredients.add(self.ingredientamount_1)
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        url = f"/api/recipes/{recipe.id}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        image = response.json().get("image")
        test_string = "http://testserver/media/recipes/images/"
        self.assertTrue(test_string in image)
        test_json = {
            "id": 2,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                },
                {
                    "id": 2,
                    "name": "test Обед",
                    "color": "#6AA84FFF",
                    "slug": "dinner",
                },
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 3,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 10,
                },
                {
                    "id": 4,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 30,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "обновленный тестовый рецепт",
            "image": image,
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        self.assertEqual(response.json(), test_json)

    def test_get_recipe_detail_unauthorized_client_401(self):
        """Обновление рецепта неавторизованным пользователем."""
        url = f"/api/recipes/{self.recipe.id}/"
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        response = self.guest_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_404(self):
        """Обновление рецепта. Страница не найдена."""
        recipe = Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            image=self.uploaded_1,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        recipe.tags.add(self.tag)
        recipe.ingredients.add(self.ingredientamount_1)
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        url = f"/api/recipes/{recipe.id + 1}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_400_without_fields(self):
        """Обновление рецепта.
        Не указаны обязательные поля."""
        recipe = Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            image=self.uploaded_1,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        recipe.tags.add(self.tag)
        recipe.ingredients.add(self.ingredientamount_1)
        data = {}
        url = f"/api/recipes/{recipe.id}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
            "image": ["Ни одного файла не было отправлено."],
            "name": ["Обязательное поле."],
            "text": ["Обязательное поле."],
            "cooking_time": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_400_negative_cookin_time(self):
        """Обновление рецепта. Ошибка валидации.
        Не валидное время готовки."""
        recipe = Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            image=self.uploaded_1,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        recipe.tags.add(self.tag)
        recipe.ingredients.add(self.ingredientamount_1)
        data = {
            "ingredients": [
                {"id": self.ingredient_1.id, "amount": 10},
                {"id": self.ingredient_2.id, "amount": 30},
            ],
            "tags": [self.tag.id, self.tag_2.id],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 0,
        }
        url = f"/api/recipes/{recipe.id}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "cooking_time": ["Убедитесь, что это значение больше либо равно 1."]
        }
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_401(self):
        """Обновление рецепта. Пользователь не авторизован."""
        pass

    def test_patch_recipe_403(self):
        """Обновление рецепта. недостаточно прав."""
        pass

    def test_delete_recipe(self):
        """Удаление рецепта."""
        url = f"/api/recipes/{self.recipe.id}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_recipe_404(self):
        """Удаление рецепта.Страница не найдена."""
        url = f"/api/recipes/{self.recipe.id + 1}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipe_401(self):
        """Удаление рецепта.Учетные данные не были предоставлены."""
        pass

    def test_delete_recipe_403(self):
        """Удаление рецепта.Недостаточно прав."""
        pass
