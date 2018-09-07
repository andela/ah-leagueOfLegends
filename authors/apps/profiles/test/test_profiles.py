from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status

class ProfileTestCase(BaseTest):

    def test_user_can_create_profile(self):
        self.register_user()
        response = self.get_profile("jake")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_non_existent_profile(self):
        pass

    def test_users_can_edit_only_their_profie(self):
        pass