from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        user_data={
            'email':'testuser@gmail.com',
            'username':'testuser',
            'password':'testuserpass',
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
