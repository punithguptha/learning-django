from django.test import TestCase
from selenium import webdriver


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

    def test_homepage_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'hashingapp/home.html')
