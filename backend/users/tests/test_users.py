from django.test import TestCase
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
