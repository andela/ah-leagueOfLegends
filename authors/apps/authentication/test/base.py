from rest_framework.test import APIClient, APITestCase


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