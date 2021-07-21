from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient  # test client to make test request
from rest_framework import status
from faker import Faker

CREATE_USER_URL = reverse('user:create-user')
TOKEN_URL = reverse('user:token')
CURRENT_USER_PROFILE_URL = reverse('user:user-profile')


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
        user_exists = get_user_model().objects.filter(email=payload.get('email')).exists()
        self.assertFalse(user_exists)

    def test_create_user_token(self):
        """
        Test token is created for user
        """

        self._create_user(**self._get_payload())
        res = self.client.post(TOKEN_URL, self._get_payload())
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_token_invalid_credentials(self):
        """
        Test invalid user credentials for creating token
        """
        payload = self._get_payload()
        self._create_user(**payload)
        payload['password'] = '7amada123'

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_anonymous_user(self):
        """
        Test token is not created for anonymous user
        """
        payload = self._get_payload()
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email & pass if required
        """

        payload = self._get_payload()
        payload['password'] = ''
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that user is always authenticated
        """
        res = self.client.get(CURRENT_USER_PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """
    Test all Api requests that require authentication
    """

    @staticmethod
    def _get_payload():
        return {
            'email': 'mina@mail.com',
            'password': 'static_pass@123',
            'first_name': 'Minos',
            'mobile': '01284782991',
            'land_line': '1122334455',
        }

    def setUp(self):
        self.faker = Faker('en')
        self.user = get_user_model().objects.create(**(self._get_payload()))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_user_profile_success(self):
        """
        Test success retrieving of current logged in user
        """

        res = self.client.get(CURRENT_USER_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        payload = self._get_payload()

        del payload['password']

        self.assertEqual(res.data, payload)

    def test_current_user_profile_post_request_not_allowed(self):
        """
        Test that post request is not allowed on the user profile url
        """

        res = self.client.post(CURRENT_USER_PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating user profile for the authenticated user
        """

        payload = self._get_payload()
        payload['first_name'] = 'New User Name'
        payload['password'] = 'Mynewpass@123'
        print('*' * 50)
        print(payload)
        res = self.client.patch(CURRENT_USER_PROFILE_URL, payload)
        print("RES -> ", res.data)

        self.user.refresh_from_db()
        print(payload.get('first_name'))
        print(self.user.first_name)

        self.assertEqual(self.user.first_name, payload.get('first_name'))
        self.assertTrue(self.user.check_password(payload.get('password')))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
