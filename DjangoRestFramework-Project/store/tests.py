from rest_framework.test import APITestCase
from store.test_setup import *
from store.models import Product
from django.conf import settings

import pdb,os
from django.urls import reverse

# Create your tests here.

class ProductCreateTestCase(TestSetUp):
    def test_create_product(self):
        initial_product_count=Product.objects.count()
        print("Inside first test case and the count is {}".format(initial_product_count))
        product_attrs={
            'name':'Test Case Product',
            'description':'Product for Test Case',
            'price':'123.45',
        }
        response=self.client.post('/api/v1/modelviewset/',product_attrs)
        if response.status_code!=201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count+1,
        )
        # Here we are iterating thorugh the key value pairs of the dict where attr stands for keys and expected_value stands for values
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(response.data['is_on_sale'],False)
        self.assertEqual(
            response.data['current_price'],
            float(product_attrs['price']),
        )

# Typically in a destroy test case contains cleanup methods..Like cache cleaning,destroying obejcts in other third party services etc
class ProductDestroyTestCase(TestSetUp):
    def test_delete_product(self):
        initial_product_count=Product.objects.count()
        print("The initial product count is {}".format(initial_product_count))
        product_id=Product.objects.first().id
        self.client.delete('/api/v1/modelviewset/{}/'.format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count-1,
        )

        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )

class ProductListTestCase(TestSetUp):
    def test_list_products(self):
        products_count=Product.objects.count()
        list_api_url=reverse("product_list_api")
        response=self.client.get(list_api_url)
        # pdb.set_trace()
        # The below two are for pagination checks. So for our data according to the pagination rules that we set we dont have any prev or next pages
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'],products_count)
        self.assertEqual(len(response.data['results']),products_count)

class ProductUpdateTestCase(TestSetUp):
    def test_update_product(self):
        product= Product.objects.first()
        # pdb.set_trace()
        response=self.client.patch(
            '/api/v1/modelviewset/{}/'.format(product.id),
            {
                'name': 'Updated TestProduct1',
                'description':'Updated description for TestProduct1',
                'price': 1.22,
            },
            format='json',
        )
        # pdb.set_trace()
        updated=Product.objects.get(id=product.id)
        self.assertEqual(updated.name,'Updated TestProduct1')

    def test_upload_product_photo(self):
        product=Product.objects.first()
        original_photo=product.photo
        photo_path=os.path.join(settings.MEDIA_ROOT,'products','vitamin-iron.jpg')
        with open(photo_path,'rb') as photo_data:
            response=self.client.patch('/api/v1/modelviewset/{}/'.format(product.id),{
                'photo':photo_data,
            },format='multipart')
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.data['photo'],original_photo)
        try:
            updated=Product.objects.get(id=product.id)
            expected_photo=os.path.join(settings.MEDIA_ROOT,'products','vitamin-iron')
            self.assertTrue(updated.photo.path.startswith(expected_photo))
        finally:
            os.remove(updated.photo.path)
