from .base import BaseTest
from django.urls import reverse
from rest_framework.views import status
from ..models import User
from ..serializers import (RegistrationSerializer,
                           LoginSerializer)


class UserAuthenticationTestCase(BaseTest):

    def test_user_registration(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred,
               format='json'
        )
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_user_login(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred,
               format='json')
        response = self.client.post(
               reverse('user_login'),
               self.user_cred,
               format='json'
        )
        print(response.data['email'])
        self.assertEquals(status.HTTP_200_OK, response.status_code)