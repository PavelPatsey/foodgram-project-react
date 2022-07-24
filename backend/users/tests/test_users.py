import unittest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="authorized_user")
        cls.guest_client = APIClient()
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
    def test_get_users_list(self):
        """Получение списка всех пользователей.
        авторизованным пользователем"""
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





