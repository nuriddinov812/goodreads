import email
from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from  django.contrib.auth import get_user

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

        user = CustomUser.objects.get(username="testuser")
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

        user_count = CustomUser.objects.count()
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

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        form = response.context["form"]
        self.assertFormError(form, "email", ["Enter a valid email address."])

    def test_unique_username(self):
        user = CustomUser.objects.create(
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
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(
            response.context["form"],
            "username",
            ["A user with that username already exists."],
        )


class LoginTestCase(TestCase):
    def setUp(self):
        # DRY principle-Don't Repeat Yourself
        self.db_user = CustomUser.objects.create(
            username="testuser",
            first_name="Test",
        )
        self.db_user.set_password("securepassword123")
        self.db_user.save()
        
    def test_successful_login(self):
        
        self.client.post(
            reverse("login"),
            data={
                "username": "testuser",
                "password": "securepassword123",
            },)
        
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
           
    def test_wrong_credentials(self):        
        response = self.client.post(
            reverse("login"),
            data={
                "username": "testuser",
                "password": "wrongpassword",
            },)
        
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated) 
        
        response = self.client.post(
            reverse("login"),
            data={
                "username": "wronguser",
                "password": "securepassword123",
            },)
        
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
            
    def test_logout(self):
        self.client.login(
            username="testuser",
            password="securepassword123",
        )
        
        self.client.get(reverse("logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
     
        
class ProfileTestCase(TestCase):
    
    def test_login_required_to_access_profile(self):
        response = self.client.get(
            reverse("profile"),
        )  
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login")+"?next=/users/profile/")  
        
    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )
        user.set_password("securepassword123")
        user.save()   
        
        
        self.client.login(
            username="testuser",
            password="securepassword123",
        )
        response = self.client.get(
            reverse("profile"),
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        
    def test_profile_edit(self):
        user = CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )
        user.set_password("securepassword123")
        user.save()
        
        self.client.login(
            username="testuser",
            password="securepassword123",
        )
        
        response = self.client.post(
            reverse("profile_edit"),
            data={
                "username": "updateduser",
                "first_name": "Updated",
                "last_name": "User",
                "email": "testuser@example.com"},
        )
        
        # user = CustomUser.objects.get(pk=user.pk)
        user.refresh_from_db()
        
        self.assertEqual(user.username, "updateduser")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(response.url, reverse("profile"))