from .test_setup import TestSetup
from ..models import User

class TestViews(TestSetup):
    def test_user_cannot_register_without_data(self):
        result=self.client.post(self.register_url)
        self.assertEqual(result.status_code,400)

    def test_user_can_register(self):
        result=self.client.post(self.register_url,self.user_data,format="json")
        self.assertEqual(result.data['email'],self.user_data['email'])
        self.assertEqual(result.data['username'],self.user_data['username'])
        self.assertEqual(result.status_code,201)

    def test_unverified_user_cannot_login(self):
        self.client.post(self.register_url,self.user_data,format="json")
        result=self.client.post(self.login_url,self.user_data,format='json')
        self.assertEqual(result.status_code,401)

    def test_verified_user_can_login(self):
        result_1=self.client.post(self.register_url,self.user_data,format="json")
        email=result_1.data['email']
        user=User.objects.get(email=email)
        user.is_verified=True
        user.save()
        result_2=self.client.post(self.login_url,self.user_data,format='json')
        self.assertEqual(result_2.status_code,200)

    # TBD
    def test_using_same_reset_link_twice_should_fail(self):
        pass

    #TBD
    def test_reset_password(self):
        pass
