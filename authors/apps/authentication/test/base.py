from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


class BaseTest(APITestCase):
    client = APIClient

    def setUp(self):
        self.user_cred = {
            "user": {
                    "email": "jake@jake.jake",
                    "username": "jake",
                    "password": "HelloWorldKen123"
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
               reverse('user_signup'),
               self.user_cred,
               format='json'
        )