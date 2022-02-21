from rest_framework.test import APITestCase
from store.models import Product

class TestSetUp(APITestCase):
    def setUp(self):
        Product.objects.create(
            name='TestProduct1',description="Product1 for unittesting",price=1.22,
        )
        Product.objects.create(
            name='TestProduct2',description="Product2 for unittesting", price=1.33,
        )
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
