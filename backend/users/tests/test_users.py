import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()
        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

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
        User.objects.create_user(
            email="vasya_pupkin@mail.com",
            username="vasya_pupkin",
            first_name="Vasya",
            last_name="Pupkin",
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
                },
                {
                    "email": "",
                    "id": 2,
                    "username": "testusername",
                    "first_name": "",
                    "last_name": "",
                },
                {
                    "email": "vasya_pupkin@mail.com",
                    "id": 3,
                    "username": "vasya_pupkin",
                    "first_name": "Vasya",
                    "last_name": "Pupkin",
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
            "id": 2,
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
            "id": 1,
            "username": "authorized_user",
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
        test_json = {'detail': 'Учетные данные не были предоставлены.'}
        self.assertEqual(response.json(), test_json)

    def test_user_profile_404(self):
        """Профиль пользователя. Страница не найдена."""
        user = User.objects.get(username="authorized_user")
        url = f"/api/users/{user.id + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {
            "detail": "Страница не найдена."
        }
        self.assertEqual(response.json(), test_json)
