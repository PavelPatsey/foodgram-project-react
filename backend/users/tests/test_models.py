from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Subscription, User


class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()
        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """Cool test."""
        self.assertEqual(True, True)

    def test_no_self_subscription(self):
        "Модель Subscription не позволяет пользователю подписаться на самого себя."
        user = User.objects.create()
        constraint_name = "prevent_self_subscription"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Subscription.objects.create(user=user, author=user)

    def test_add_recipe_to_shopping_cart_authorized_client(self):
        """Подписаться авторизованным пользователем."""
        count = Subscription.objects.count()
        test_user = User.objects.create_user(username="test_username")
        url = f"/api/users/{test_user.id}/subscribe/"
        breakpoint()
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        test_json = {}
        self.assertEqual(response.json(), test_json)
