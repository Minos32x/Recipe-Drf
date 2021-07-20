from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient  # test client to make test request
from rest_framework import status
from faker import Faker

CREATE_USER_URL = reverse('user:create-user')


class PublicUserApiTest(TestCase):

    def _create_user(self, **kwargs):
        return get_user_model().objects.create_user(**kwargs)

    def setUp(self) -> None:
        self.faker = Faker('en')
        self.client = APIClient()

    def _get_payload(self):
        return {
            'email': 'static@mail.com',
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def test_create_valid_user_success(self):
        # self._create_user(payload)
        res = self.client.post(CREATE_USER_URL, self._get_payload())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        print(res.data)

        user = get_user_model().objects.get(**res.data)

        # Make sure password is same as created
        self.assertTrue(user.check_password(self._get_payload().get('password')))
        # Make sure that password is not returned in the response for security
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test if user already exists
        """
        self._create_user(**self._get_payload())

        res = self.client.post(CREATE_USER_URL, self._get_payload())
        print("TEST USER EXISTS RES -> ", res)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test on password if too short
        """
        payload = self._get_payload()
        payload['password'] = '1234'

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)
