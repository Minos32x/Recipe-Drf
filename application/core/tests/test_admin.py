from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker


class AdminSiteTest(TestCase):

    def setUp(self) -> None:
        """
        This is the setup that will run every time i run this test class
        """
        # Fake data generator
        self.faker = Faker('en')

        # Initiate a web client
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email=self.faker.email(), password=self.faker.password(),
            land_line=self.faker.phone_number(),
            mobile=self.faker.phone_number()
        )

        self.user = get_user_model().objects.create_user(
            email=self.faker.email(), password=self.faker.password(),
            land_line=self.faker.phone_number(),
            mobile=self.faker.phone_number()
        )

        self.client.force_login(self.admin_user)

    def test_user_listed(self):
        """
        Test that users are listed well
        """
        url = reverse('admin:core_user_changelist')
        result = self.client.get(url)

        self.assertContains(result, self.user.email)
        self.assertContains(result, self.user.first_name)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
        self.assertContains(result, self.user.email)
        self.assertContains(result, self.user.first_name)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
