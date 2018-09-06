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
                "password": "J!ake123456"
            }
        }

        self.user_cred_wrong_pass = {
            "user": {
                    "email": "jake@jake.jake",
                    "username": "jake",
                    "password": "some_fake_password"
                }
        }

        self.user_cred_no_email = {
            "user": {
                    "email": "",
                    "username": "jake",
                    "password": "HelloWorldKen123"
                }
        }

        self.user_cred_no_username = {
            "user": {
                    "email": "",
                    "username": "",
                    "password": "HelloWorldKen123"
                }
        }

        self.user_cred_no_details = {
            "user": {
                    "email": "",
                    "username": "",
                    "password": ""
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