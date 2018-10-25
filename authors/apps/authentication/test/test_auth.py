from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status
from ..models import User


class UserAuthenticationTestCase(BaseTest):

    def test_user_can_register(self):
        """Test whether user gets a valid token on registration"""
        response = self.client.post(
            reverse('authentication:user_signup'),
            self.user_cred,
            format='json'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_user_receives_token_on_registration(self):
        pass

    def test_verification_email_sent_on_registration(self):
        pass

    def test_user_registration_no_email(self):
        response = self.client.post(
            reverse('authentication:user_signup'),
            self.user_cred_no_email,
            format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_registration_no_username(self):
        response = self.client.post(
            reverse('authentication:user_signup'),
            self.user_cred_no_username,
            format='json'
        )
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_registration_no_details(self):
        response = self.client.post(
            reverse('authentication:user_signup'),
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
            reverse('authentication:user_signup'),
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json'
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred_wrong_pass,
            format='json')

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_password_reset_with_no_email(self):
        response = self.client.post(
            self.RESET_PASS,
            self.no_email,
            format='json'
        )
        expected = {'message': "Password reset failed. Please check your email and try again"}
        self.assertEquals(response.data, expected)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_password_reset_with_wrong_email(self):
        response = self.client.post(
            self.RESET_PASS,
            self.wrong_email,
            format='json'
        )
        expected = {'message': "Password reset failed. Please check your email and try again"}
        self.assertEquals(response.data, expected)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_password_reset_with_correct_email(self):
        response = self.register_user()
        response = self.login_user()
        response = self.client.post(
            self.RESET_PASS,
            self.correct_email,
            format='json'
        )
        expected = {'message': "Reset Link successfully sent to your Email"}
        self.assertEquals(response.data, expected)
        self.assertEquals(status.HTTP_200_OK, response.status_code)