from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTester(TestCase):

    def tes_user_creation(self):
        """
        Test creating a new user using email
        """
        mail = 'testuser@mail.com'
        password = 'test12345'

        user = get_user_model().objects.create_user(
            email=mail, password=password,
        )

        self.assertEqual(user.email, mail)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        email = 'minos@Z2BOLA.COM'
        user = get_user_model().objects.create_user(
            email=email, password='mesho1234'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test invalid user email creation
        """

        with self.assertRaises(ValueError):
            email = None
            password = 'memo1234'
            get_user_model().objects.create_user(
                email=email, password=password)

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            email='mysuper@app.com',
            password='test@123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
