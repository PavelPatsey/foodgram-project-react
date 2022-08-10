import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import Subscription, User


class UsersViewsTest(TestCase):
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
        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name="test рецепт",
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe.tags.add(cls.tag)
        cls.recipe.ingredients.add(
            cls.ingredientamount_1,
            cls.ingredientamount_2,
        )
        cls.recipe_2 = Recipe.objects.create(
            author=cls.user,
            name="test рецепт 2",
            text="описание тестового рецепта 2",
            cooking_time=10,
        )
        cls.recipe_2.tags.add(cls.tag)
        cls.recipe_2.ingredients.add(
            cls.ingredientamount_1,
            cls.ingredientamount_2,
        )

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_users_list_unauthorized_user(self):
        """Получение списка всех пользователей.
        неавторизованным пользователем"""
        url = "/api/users/"
        User.objects.create_user(username="testusername")
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @unittest.expectedFailure
    def test_get_users_list_without_paginator(self):
        """Получение списка всех пользователей.
        Без паджинации."""
        url = "/api/users/"
        User.objects.create_user(username="testusername")
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = [
            {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
            }
        ]
        self.assertEqual(response.json(), test_json)

    def test_get_users_list(self):
        """Получение списка всех пользователей авторизованным пользователем."""
        url = "/api/users/"
        User.objects.create_user(username="testusername")
        user = User.objects.create_user(
            email="vasya_pupkin@mail.com",
            username="vasya_pupkin",
            first_name="Vasya",
            last_name="Pupkin",
        )
        Subscription.objects.create(
            user=self.user,
            author=user,
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "email": "",
                    "id": 1,
                    "username": "authorized_user",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "",
                    "id": 2,
                    "username": "testusername",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "vasya_pupkin@mail.com",
                    "id": 3,
                    "username": "vasya_pupkin",
                    "first_name": "Vasya",
                    "last_name": "Pupkin",
                    "is_subscribed": True,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user(self):
        """Регистрация пользователя."""
        url = "/api/users/"
        users_count = User.objects.count()
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_count + 1)
        test_json = {
            "email": "vpupkin@yandex.ru",
            "id": users_count + 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_with_simple_password(self):
        """Регистрация пользователя с простым паролем."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "123",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "password": [
                "Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.",
                "Введённый пароль слишком широко распространён.",
                "Введённый пароль состоит только из цифр.",
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_without_password(self):
        """Регистрация пользователя без пароля."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"password": ["Обязательное поле."]})

    def test_create_user_without_email(self):
        """Регистрация пользователя без почты."""
        url = "/api/users/"
        data = {
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Обязательное поле."]})

    def test_create_user_without_username(self):
        """Регистрация пользователя без имени пользователя."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"username": ["Обязательное поле."]})

    def test_create_user_without_first_name(self):
        """Регистрация пользователя без first_name."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"first_name": ["Обязательное поле."]})

    def test_create_user_without_last_name(self):
        """Регистрация пользователя без last_name."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"last_name": ["Обязательное поле."]})

    def test_create_user_without_first_last_names(self):
        """Регистрация пользователя без имени и фамилии."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"first_name": ["Обязательное поле."], "last_name": ["Обязательное поле."]},
        )

    def test_user_profile(self):
        """Профиль пользователя."""
        user = User.objects.get(username="authorized_user")
        url = f"/api/users/{user.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "",
            "id": user.id,
            "username": "authorized_user",
            "is_subscribed": False,
            "first_name": "",
            "last_name": "",
        }
        self.assertEqual(response.json(), test_json)

    def test_user_profile_by_unauthorized_user(self):
        """Профиль пользователя.
        Учетные данные не были предоставлены."""
        user = User.objects.get(username="authorized_user")
        url = f"/api/users/{user.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_user_profile_404(self):
        """Профиль пользователя. Страница не найдена."""
        user = User.objects.get(username="authorized_user")
        url = f"/api/users/{user.id + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile(self):
        """Профиль текущего пользователя."""
        user = User.objects.get(username="authorized_user")
        url = "/api/users/me/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "",
            "id": user.id,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": False,
        }
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile_401(self):
        """Профиль текущего пользователя.
        401 пользователь не авторизован."""
        url = "/api/users/me/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_set_password(self):
        """Изменение пароля."""
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "1wkfy267snsndndnd",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_password_incorrect_current_password(self):
        """Изменение пароля. Некорректный текущий пароль."""
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "123",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"current_password": ["Неправильный пароль."]}
        self.assertEqual(response.json(), test_json)

    def test_set_password_401(self):
        """Изменение пароля. 401 пользователь не авторизован."""
        url = "/api/users/set_password/"
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "1wkfy267snsndndnd",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_get_authorization_token(self):
        """Получить токен авторизации."""
        url = "/api/auth/token/login/"
        User.objects.create_user(
            username="test_user", password="1wkfy267snsndndnd", email="test@mail.ru"
        )
        data = {"password": "1wkfy267snsndndnd", "email": "test@mail.ru"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("auth_token" in response.json().keys())

    def test_get_authorization_token_with_invalid_data(self):
        """Получить токен авторизации с невалидными данными."""
        url = "/api/auth/token/login/"
        data = {"password": "string", "email": "string"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "non_field_errors": [
                "Невозможно войти с предоставленными учетными данными."
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_deleting_token(self):
        """Удаление токена."""
        url = "/api/auth/token/logout/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_token_401(self):
        """Удаление токена. 401 пользователь не авторизован."""
        url = "/api/auth/token/logout/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_authorized_client(self):
        """Подписаться авторизованным пользователем."""
        test_user = User.objects.create_user(username="test_username")
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        test_json = {
            "email": "",
            "id": 1,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": True,
            "recipes": [
                {"id": 2, "name": "test рецепт 2", "image": None, "cooking_time": 10},
                {"id": 1, "name": "test рецепт", "image": None, "cooking_time": 4},
            ],
            "recipes_count": 2,
        }
        self.assertEqual(response.json(), test_json)
