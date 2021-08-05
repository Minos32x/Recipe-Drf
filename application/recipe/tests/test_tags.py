from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recipe.serializers import TagSerializer

from recipe.models import (Tag)
import faker

TAGS_LIST_URL = reverse('recipe:tag-list')
TAG_CREATE_URL = reverse('recipe:tag-create')
TAG_UPDATE_URL = reverse('recipe:tag-update')


class TagsTest(TestCase):

    def setUp(self) -> None:
        self.faker = faker.Faker('en')

    def _get_user_data(self):
        return {
            'email': 'static@mail.com',
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def _get_create_user(self):
        return get_user_model().objects.create_user(**self._get_user_data())

    def test_str_tags(self):
        tag_res = Tag.objects.create(user=self._get_create_user(), name='Vegan')
        self.assertEqual(str(tag_res), tag_res.name)


class PublicApiTagsTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required_to_retrieve_tags(self):
        res = self.client.get(TAGS_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTagsTest(TestCase):

    def _get_user_data(self):
        return {
            'email': self.faker.email(),
            'password': self.faker.password(),
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def _create_user(self):
        return get_user_model().objects.create_user(**self._get_user_data())

    def setUp(self) -> None:
        self.faker = faker.Faker('en')
        self.user = self._create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags_authenticated(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_LIST_URL)
        tags = Tag.objects.all().order_by('-name')
        serialized_tags = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print('TAGS LIST FROM API->', res.data)
        print('TAGS LIST FROM ORM', serialized_tags.data)
        self.assertEqual(res.data, serialized_tags.data)

    def test_tag_limited_to_user(self):
        """
        Test that tags retrieved are for the authenticated user
        """
        other_user = self._create_user()
        Tag.objects.create(user=other_user, name='FRUIT')
        Tag.objects.create(user=other_user, name='MEAT')

        res = self.client.get(TAGS_LIST_URL)
        tags = Tag.objects.filter(user=self.user).order_by('-name')
        serialized_tags = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # self.assertNotEqual(serialized_tags.data.user, self.user)

    def test_create_tag_success(self):
        payload = {'name': 'xxxx'}

        res = self.client.post(TAG_CREATE_URL, payload)
        print(res.status_code)
        print(res)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_tag_invalid(self):
        payload = {"name": ""}
        res = self.client.post(TAG_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
