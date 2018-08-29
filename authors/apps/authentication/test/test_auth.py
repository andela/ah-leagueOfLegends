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

    def test_user_registration_no_email(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred_no_email,
               format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_registration_no_username(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred_no_username,
               format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)


    def test_user_registration_no_details(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred_no_details,
               format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_double_registration(self):
        response = self.register_user()
        response = self.register_user()
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

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

        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_login_wrong_password(self):
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred,
               format='json')
        response = self.client.post(
               reverse('user_signup'),
               self.user_cred_wrong_pass,
               format='json')

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
