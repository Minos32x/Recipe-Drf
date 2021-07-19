from faker import Faker

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTester(TestCase):

    def setUp(self) -> None:
        self.faker = Faker('en')

    def _get_random_email(self):
        return self.faker.first_name_male()

    def _get_random_user_name(self):
        return self.faker.first_name_male().lower()

    def _generate_random_mobile(self):
        return self.faker.phone_number()

    def _generate_random_land_line(self):
        return self.faker.phone_numer()

    def test_new_user_creation(self):
        """
        Test creating a new user using email
        """
        mail = self.faker.email().lower()
        password = self.faker.password()

        user = get_user_model().objects.create_user(
            email=mail, password=password,
        )

        self.assertEqual(user.email, mail)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'minos@Z2BOLA.COM'
        user = get_user_model().objects.create_user(
            email=email, password='mesho1234'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test invalid user email creation
        """
        print("Testing : new user invalid email")
        with self.assertRaises(ValueError):
            email = None
            password = self.faker.password()
            get_user_model().objects.create_user(
                email=email, password=password)

    def test_create_super_user(self):
        print("Testing : create super user")
        user = get_user_model().objects.create_superuser(
            email=self.faker.email(),
            password=self.faker.password())

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
