from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

class BaseTest(APITestCase):
    client = APIClient

    def setUp(self):
        self.SIGN_UP_URL = '/api/users/'

        self.user_cred = {
            "user": {
                    "email": "jake@jake.jake",
                    "username": "jake",
                    "password": "jake123456"
                }
        }

    def register_user(self):
        return self.client.post(
               self.SIGN_UP_URL,
               self.user_cred,
               format='json'
        )
    def login_user(self):
        return self.client.post(
               self.SIGN_UP_URL,
               self.user_cred,
               format='json'
        )