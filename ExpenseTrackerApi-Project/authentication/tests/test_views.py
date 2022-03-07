from .test_setup import TestSetup

class TestViews(TestSetup):
    def test_user_cannot_register_without_data(self):
        result=self.client.post(self.register_url)
        self.assertEqual(result.status_code,400)
    
