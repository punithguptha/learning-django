from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import HashModel
import pdb

# class FunctionalTestCase(TestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#
#     def test_homepage(self):
#         self.browser.get('http://localhost:8000')
#         self.assertIn("Enter hash here:",self.browser.page_source)
#
#     def test_hash_of_hello(self):
#         self.browser.get('http://localhost:8000')
#         text=self.browser.find_element(by='id',value='id_text')
#         text.send_keys("hello")
#         self.browser.find_element(by='name',value='submit').click()
#         # The logic which we are using here is SHA256 Encryption to hash the text the the user types in the site
#         self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',self.browser.page_source)
#
#     def tearDown(self):
#         self.browser.quit()

class UnitTestCase(TestCase):

    # A test has to always start with test_

    def setUp(self):
        HashModel.objects.create(
            text='hello',hashed_text='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
        )
        return super().setUp()

    def test_homepage_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'hashingapp/home.html')

    def test_hash_form(self):
        form=HashForm(data={'text':'hello'})
        # Is Valid is an internal function offered by django forms which basically checks whether all the fields of the form are valid
        self.assertTrue(form.is_valid())

    def test_hash_function(self):
        text_hash=hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',text_hash)

    def test_hash_model(self):
        pulled_hash=HashModel.objects.get(hashed_text='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(pulled_hash.text,'hello')

    # In this test we are checking for our url format hash/hashed_string which should contain the original text in its view
    def test_view(self):
        response=self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824/')
        self.assertContains(response,'hello')

    def tearDown(self):
        return super().tearDown()
