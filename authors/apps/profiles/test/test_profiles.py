from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status

class ProfileTestCase(BaseTest):
    image ={
        "user": {
             "image": "https://vsco.co/tichtoo/media/544f6752726708181b8b4a76"
            }
            }
    bio ={
            "user": {
                "bio":"Through the lense",
            }
            }
        
    def update_user_bio(self, token,bio):
        """Helper method to update an user bio"""
        return self.client.put(
            '/api/user/',
            bio,
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
    def update_user_image(self, token,image):
        """Helper method to update an user image"""
        return self.client.put(
            '/api/user/',
            image,
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )

    def test_user_can_create_profile(self):
        """ Test if user profile is created """ 
        self.register_user()
        response = self.get_profile("jake")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_non_existent_profile(self):
        """
        Test wether the appropriate message is returned upon searching a
        non-existent profile
        """
        response = self.get_profile("whodat")
        expected = "The requested profile does not exist."
        self.assertTrue(response.data['errors']['detail'] == expected)

    
    def test_update_bio(self):
            """ 
            Tests whether a user can update his/her profile bio
            """
            self.register_user()
            response = self.login_user()
            token = response.data['token']
            response = self.update_user_bio(token,self.bio)
            self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_update_image(self):
            """ 
            Tests whether a user can update his/her profile bio
            """
            self.register_user()
            response = self.login_user()
            token = response.data['token']
            response = self.update_user_image(token,self.image)
            self.assertEquals(status.HTTP_200_OK, response.status_code)
    