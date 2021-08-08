from django.test import TestCase
import faker
from recipe.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import reverse

RECIPE_LIST_URL = reverse('recipe:recipe-list')


# RECIPE_CREATE_URL = reverse('recipe:recipe-create')
# RECIPE_UPDATE_URL = reverse('recipe:recipe-update')
# RECIPE_VIEW_URL = reverse('recipe:recipe-view')


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
            'price': 5.00, 'title': 'Pizza', 'user': self.user, 'time_in_minutes': 5
        }

    def setUp(self) -> None:
        self.faker = faker.Faker('en')
        self.client = APIClient()
        self.user = get_user_model().objects.create(**self._get_user_data())

    def test_recipe_str(self):
        recipe = Recipe.objects.create(**self._get_recipe_data())
        self.assertEqual(str(recipe.title), recipe.title)


class TestRecipeAPiPublic(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_recipe_auth_required(self):
        res = self.client.get(RECIPE_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestRecipePrivateApi(TestCase):

    def _get_user_data(self):
        return {
            'email': self.faker.email(),
            'password': 'static_pass@123',
            'first_name': self.faker.first_name_male().lower(),
            'mobile': self.faker.phone_number(),
            'land_line': self.faker.phone_number(),
        }

    def _get_recipe_data(self, kwargs):
        data = {
            'title': 'Pizza',
            'price': 5.00,
            'time_in_minutes': 10,
            'user': self.user
        }
        data.update(kwargs)
        return data

    def _create_recipe(self, **kwargs):
        return Recipe.objects.create(**self._get_recipe_data(kwargs))

    def setUp(self):
        self.client = APIClient()
        self.faker = faker.Faker('en')
        self.user = get_user_model().objects.create(**self._get_user_data())
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieving recipe list"""
        self._create_recipe(title='Burger')
        self._create_recipe(title='Alfredo')

        res = self.client.get(RECIPE_LIST_URL)

        all_recipes = Recipe.objects.all()
        serialized_recipes = RecipeSerializer(all_recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_recipes.data)

    def test_recipes_limited_to_user(self):
        new_user = get_user_model().objects.create(**self._get_user_data())

        self._create_recipe(user=new_user, title='Pizza')
        self._create_recipe(title='Macaroni')

        res = self.client.get(RECIPE_LIST_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serialized_recipes = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data, serialized_recipes.data)

    def _create_tags(self, tag='Pizza Section', user=None):
        if not user:
            user = self.user
        return Tag.objects.create(name=tag, user=user)

    def _create_ingredients(self, name='Tomato', user=None):
        if not user:
            user = self.user
        return Ingredient.objects.create(name=name, user=user)

    @staticmethod
    def _detail_url(recipe_id):
        return reverse('recipe:recipe-detail', args=[recipe_id])

    def test_recipe_detail(self):
        """ Test View Recipe Detail"""
        recipe = Recipe.objects.create(**self._get_recipe_data({}))

        recipe.tags.add(self._create_tags())
        recipe.ingredients.add(self._create_ingredients())

        url = self._detail_url(recipe.id)
        res = self.client.get(url)

        serialized_data = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serialized_data.data)

    def test_create_recipe(self):
        payload = {'title': 'Chocolate Cacke', 'price': 10, 'time_in_minutes': 20}
        res = self.client.post(RECIPE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(pk=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        tag1 = self._create_tags(tag='Dessert', user=self.user)
        tag2 = self._create_tags(tag='Dinner')

        payload = {
            'title': 'Avocado Lime Cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_in_minutes': 25,
            'price': 20.95
        }

        res = self.client.post(RECIPE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(pk=res.data['id'])

        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)

        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        ingredient1 = self._create_ingredients(name='Cheese')
        ingredient2 = self._create_ingredients(name='Flavor')
        payload = {
            'title': 'Crunshy', 'price': 2.5, 'time_in_minutes': 15,
            'ingredients': [ingredient1.id, ingredient2.id]
        }

        res = self.client.post(RECIPE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(pk=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)

        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_recipe_partial_update(self):
        recipe = self._create_recipe()
        recipe.tags.add(self._create_tags())
        new_tag = self._create_tags(tag='New Tag')

        payload = {
            'title': 'Chicken Tikka',
            'tags': [new_tag.id]
        }

        url = self._detail_url(recipe.id)

        self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload.get('title'))

        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 1)

        self.assertIn(new_tag, tags)

    def test_recipe_full_update(self):
        """
        Using put method it will replace the existing object with the newly sent one it will remove any field that
        if being excluded from the request
        """

        recipe = self._create_recipe()
        recipe.tags.add(self._create_tags())
        payload = {
            'title': 'spaghetti',
            'time_in_minutes': 20,
            'price': 8.75
        }
        url = self._detail_url(recipe.id)

        self.client.put(url, payload)
        recipe.refresh_from_db()

        self.assertEqual(recipe.title, payload.get('title'))
        self.assertEqual(recipe.time_in_minutes, payload.get('time_in_minutes'))
        self.assertEqual(recipe.price, payload.get('price'))

        self.assertEqual(recipe.tags.all().count(), 0)
