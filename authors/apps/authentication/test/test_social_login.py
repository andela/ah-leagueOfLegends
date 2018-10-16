from __future__ import unicode_literals
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
import os


class SocialAuthenticationTests(APITestCase):
    def setUp(self):
        """
        Setup for tests
        """
        # Set up the social_auth url.
        self.auth_url = reverse('authentication:social_auth')
        self.client = APIClient()

    def test_new_user_signup(self):
        """
        Test signing up of new user
        """
        access_token = os.getenv("test_twitter_access_token")
        access_token_secret = os.getenv("test_twitter_access_token_secret")
        data = {"provider": "twitter", "access_token": access_token,
                "access_token_secret": access_token_secret}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_missing_access_token(self):
        """
        Test request without passing the access token
        """
        data = {"provider": "github"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_provider(self):
        """
        Test request without passing the provider
        """
        access_token = "7e19b118feb4357fe0057a2e8a6c9f9cea668552"
        data = {"access_token": access_token}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_provider(self):
        """
        Test giving a non-existent provider
        """
        access_token = "authorshaven"
        data = {"access_token": access_token, "provider": "facebook-oauth23"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_token(self):
        """
        Test an invalid access token
        """
        access_token = "authorshaven"
        data = {"access_token": access_token, "provider": "facebook"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)
