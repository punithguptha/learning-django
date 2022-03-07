from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

class TestSetup(APITestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.fake_data_generator=Faker()
        Faker.seed(0)
        self.user_data={
            'email': self.fake_data_generator.email(),
            'username': self.fake_data_generator.first_name(),
            # https://faker.readthedocs.io/en/master/providers/faker.providers.misc.html?highlight=password#faker.providers.misc.Provider.password
            'password': self.fake_data_generator.password(length=20,special_chars=False),
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
