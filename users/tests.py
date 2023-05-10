from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "sherzod",
                "first_name": "Sherzod",
                "last_name": "Majidov",
                "email": "majidov_dev@mail.ru",
                "password": "pswd123"
            }
        )

        user = CustomUser.objects.get(username="sherzod")
        self.assertEqual(user.first_name, "Sherzod"),
        self.assertEqual(user.last_name, "Majidov"),
        self.assertEqual(user.email, "majidov_dev@mail.ru"),
        self.assertNotEqual(CustomUser.password, "pswd123"),
        self.assertTrue(user.check_password("pswd123"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Sherzod",
                "email": "majidov_dev@mail.ru",
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "sherzod",
                "first_name": "Sherzod",
                "last_name": "Majidov",
                "email": "majidov_dev",
                "password": "pswd123"
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "sherzod",
                "first_name": "Sherzod",
                "last_name": "Majidov",
                "email": "majidov_dev@mail.ru",
                "password": "pswd123"
            }
        )
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "sherzod",
                "first_name": "Shaxzod",
                "last_name": "Majidov",
                "email": "shaxzod_majidov@mail.ru",
                "password": "pswd123"
            }
        )
        users_count = CustomUser.objects.count()
        self.assertEqual(users_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    # DRY - don't repeat yourself
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(username="sherzod", first_name="Sherzod")
        self.db_user.set_password("pswd123")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":"sherzod",
                "password": "pswd123"
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "pswd123"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated) # must be false

        self.client.post(
            reverse("users:login"),
            data={
                "username": "sherzod",
                "password": "wrong-password"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)  # must be false

    def test_logout(self):
        self.client.login(username="sherzod", password="pswd123")
        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create_user(username="sherzod", first_name="Sherzod")
        user.set_password("pswd123")
        user.save()

        self.client.login(username="sherzod", password="pswd123")

        response = self.client.get(reverse("users:profile"))
        self.assertContains(response, user.username)

    def test_update_profile(self):
        user = CustomUser.objects.create_user(username="sherzod", first_name="Sherzod", last_name="Majidov", email="test@mail.ru")
        user.set_password("pswd123")
        user.save()

        self.client.login(username="sherzod", password="pswd123")

        respones = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "agwemis",
                'first_name': "Shaxzod",
                'last_name': "Majidov",
                'email': "test@mail.ru"
            }
        )
        user = CustomUser.objects.get(id=user.pk)
        # yoki user = CustomUser.refresh_from_db()

        self.assertEqual(user.username, "agwemis")
        self.assertEqual(user.first_name, "Shaxzod")
        self.assertEqual(respones.url, reverse("users:profile"))





















