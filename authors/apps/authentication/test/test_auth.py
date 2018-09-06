from django.urls import reverse
from rest_framework.views import status
from django.core import mail
from rest_framework.authtoken.models import Token

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from ..models import User
from ..views import Verify
from authors.apps.base_test import BaseTest
from ..chk_token import authcheck_token


class EmailAuthenticationTestCase(BaseTest):

    def test_email_is_sent(self):
        self.register_user()
        self.assertEquals(len(mail.outbox), 1)

    def test_user_can_reset_password(self):
        '''Test registered users can reset their password by sending token
        reset token to their emails.
        '''
        response = self.register_user()
        user = User.objects.get()
        token = authcheck_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8")
        request = APIRequestFactory().get(
            reverse("authentication:verify", args=[uid, token]))
        verify_account = Verify.as_view()
        response = verify_account(request, uidb64=uid, token=token)
        self.assertTrue(response.status_code, 200)
        user = User.objects.get()
        self.assertTrue(user.confirmed_user)

    def test_user_acccount_verified(self):
        '''Test if the user email account is verified, by checking if the
        confirmed_user status is true or false
        '''
        response = self.register_user()
        user = User.objects.get()
        token = authcheck_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8")
        request = APIRequestFactory().get(
            reverse("authentication:verify", args=[uid, token]))
        verify_account = Verify.as_view()
        response = verify_account(request, uidb64=uid, token=token)
        self.assertTrue(response.status_code, 200)
        user = User.objects.get()
        self.assertTrue(user.confirmed_user)

    def test_user_enters_invalid_token(self):
        '''Test for invalid verification token when the user tries to
        reset password
        '''
        self.register_user()
        user = User.objects.get()
        token = authcheck_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(113791)).decode("utf-8")
        request = APIRequestFactory().get(
            reverse("authentication:verify", args=[uid, token]))
        verify_account = Verify.as_view()
        response = verify_account(request, uidb64=uid, token=token)
        self.assertTrue(response.status_code, 200)
        user = User.objects.get()
        self.assertFalse(user.confirmed_user)
