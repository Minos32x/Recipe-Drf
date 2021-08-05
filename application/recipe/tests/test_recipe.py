from django.test import TestCase
import faker
from recipe.models import Recipe
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class TestRecipeModel(TestCase):

    def _get_user_data(self):
        return {
            'email': self.faker.email(),
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def _get_recipe_data(self):
        return {
            'price': 5.0, 'title': 'Pizza', 'user': self.user, 'time_in_minutes': 5
        }

    def setUp(self) -> None:
        self.faker = faker.Faker('en')
        self.client = APIClient()
        self.user = get_user_model().objects.create(**self._get_user_data())

    def test_recipe_str(self):
        recipe = Recipe.objects.create(**self._get_recipe_data())
        self.assertEqual(str(recipe.title), recipe.title)
