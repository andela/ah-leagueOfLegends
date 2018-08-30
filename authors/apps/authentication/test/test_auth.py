from .base import BaseTest
from django.urls import reverse
from rest_framework.views import status
from ..models import User

class UserAuthenticationTestCase(BaseTest):

    def test_user_registration_token(self):
        """Test whether user gets a valid token on registration"""
        response = self.client.post(
               reverse('authentication:user_signup'),
               self.user_cred,
               format='json'
        )
        self.assertTrue(len(response.data['token'].split(".")) == 3)

    def test_user_login_token(self):
        """Test whether user gets a valid token on login"""
        response = self.client.post(
               reverse('authentication:user_signup'),
               self.user_cred,
               format='json'
        )
        self.assertTrue(len(response.data['token'].split(".")) == 3)
