from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import reverse
from recipe.models import Ingredient
from django.contrib.auth import get_user_model
import faker
from recipe.serializers import IngredientSerializer

INGREDIENT_CREATE_URL = reverse('recipe:ingredient-create')
INGREDIENT_LIST_URL = reverse('recipe:ingredient-list')
INGREDIENT_UPDATE_URL = reverse('recipe:ingredient-update')


class TestIngredientModel(TestCase):

    def _get_user_data(self):
        return {
            'email': 'static@mail.com',
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def setUp(self) -> None:
        self.faker = faker.Faker('en')
        self.user = get_user_model().objects.create(**self._get_user_data())

    def test_create_ingredient_object(self):
        """
        Test create object from model directly
        """
        res = Ingredient.objects.create(user=self.user, name='TEST MODEL INGREDIENT')

        self.assertEqual(str(res.name), res.name)


class TestPublicIngredientApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_request(self):
        res = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestIngredientApi(TestCase):

    def _get_user_data(self):
        return {
            'email': self.faker.email(),
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def setUp(self) -> None:
        self.faker = faker.Faker('en')
        self.client = APIClient()
        self.user = get_user_model().objects.create(**self._get_user_data())
        self.client.force_authenticate(self.user)

    def test_create_ingredient(self):
        """
        Test create from api
        """
        res = self.client.post(INGREDIENT_CREATE_URL, {'name': 'Cucumber-A'})
        ingredient = Ingredient.objects.filter(user=self.user, name='Cucumber-A').exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ingredient)

    def test_list_ingredient(self):
        res = self.client.get(INGREDIENT_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_list_ingredient(self):
        Ingredient.objects.create(user=self.user, name='T1')
        Ingredient.objects.create(user=self.user, name='T2')

        res = self.client.get(INGREDIENT_LIST_URL)

        serialized = IngredientSerializer(instance=Ingredient.objects.all(), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized.data, res.data)

    def test_ingredient_limited_to_user(self):
        user2 = get_user_model().objects.create(**self._get_user_data())

        Ingredient.objects.create(user=user2, name='Salt')
        ing = Ingredient.objects.create(user=self.user, name='Vinger')

        res = self.client.get(INGREDIENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)

    # def test_update_ingredient(self):
    #     payload = {'name': 'Name Modified'}
    #     res = self.client.patch(INGREDIENT_UPDATE_URL)


