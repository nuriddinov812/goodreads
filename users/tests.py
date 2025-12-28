from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.


class RegistrationTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(
            reverse("register"),
            data={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
                "password": "securepassword123",
            },
        )

        user = User.objects.get(username="testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("securepassword123"))

    def test_required_fiels(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "testuser",
                "email": "testuser@example.com",
            },
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        form = response.context["form"]
        self.assertFormError(form, "first_name", ["This field is required."])
        self.assertFormError(form, "password", ["This field is required."])

    def test_valid_email(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "invalid-email",
                "password": "securepassword123",
            },
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        form = response.context["form"]
        self.assertFormError(form, "email", ["Enter a valid email address."])

    def test_unique_username(self):
        user = User.objects.create(
            username="testuser",
            first_name="Test",
        )
        user.set_password("somepassword")
        user.save()

        response = self.client.post(
            reverse("register"),
            data={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
                "password": "securepassword123",
            },
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(
            response.context["form"],
            "username",
            ["A user with that username already exists."],
        )
