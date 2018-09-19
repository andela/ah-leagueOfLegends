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
    # helper methods  
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
    def retrieve_profiles(self, token):
        """Helper method to update an user bio"""
        return self.client.get(
            '/api/profiles',
            HTTP_AUTHORIZATION='Bearer ' + token,
        )

    def follow_user(self, token,username):
        """Helper method to follow a user """
        return self.client.put(
            '/api/profiles/'+ username +'/follow',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
    def get_profile_with_authentication(self, token,username):
        """Helper method to retrieve a profile with authentication"""
        return self.client.get(
            '/api/profiles/'+ username,
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
    def list_followers(self, token,username):
        """Helper method to show followers of a user """
        return self.client.get(
            '/api/profiles/'+ username +'/followers',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
    def list_following(self, token,username):
        """Helper method to show profiles user is following"""
        return self.client.get(
            '/api/profiles/'+ username +'/following',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )

    # unit tests
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
    
    def test_list_profiles(self):
        """ 
        Tests whether a user profile can be listed after authentication.
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.retrieve_profiles(token)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_list_profiles_without_authentication(self):
        """ 
        Tests whether a user profile can be listed without authentication.
        """
        self.register_user()
        token = ''
        response = self.retrieve_profiles(token)
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_paginated_profile_list(self):
        """
        Test user can view paginated data
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.retrieve_profiles(token)
        self.assertEquals(response.data['count'], 1)
    # following unit tests
    def test_follow_user(self):
        """ 
        Tests whether a user can follow a profile 
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # login jake
        response = self.login_user()
        token = response.data['token']
        response = self.follow_user(token,"jakerrrrrr")
        self.assertTrue(response.data['following'])
        self.assertEquals(status.HTTP_200_OK, response.status_code)
    
    def test_follow_user_without_authentication(self):
        """ 
        Tests whether a user can follow a profile without authentication
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        token = ''
        response = self.follow_user(token,"jakerrrrrr")
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_cant_follow_oneself(self):
        """ Tests whether a user cant follow himself/herself """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.follow_user(token,"jake")
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_follow_non_existent_user(self):
        """ 
        Tests whether a user can follow a non_existent_profile 
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.follow_user(token,"Mrs.non_existent_user")
        expected = "The requested profile does not exist."
        self.assertTrue(response.data['errors']['detail'] == expected)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    # unfollowing unit tests
    def test_ufollow_user(self):
        """ 
        Tests whether a user can unfollow a profile 
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # login jake
        response = self.login_user()
        token = response.data['token']
        self.follow_user(token,"jakerrrrrr")
        # send request again to unfollow a user
        response = self.follow_user(token,"jakerrrrrr")
        self.assertFalse(response.data['following'])
        self.assertEquals(status.HTTP_200_OK, response.status_code)
    
    def test_unfollow_non_existent_user(self):
        """ 
        Tests whether a user can unfollow a non_existent_profile 
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        self.follow_user(token,"non_existent_user")
        response = self.follow_user(token,"Mrs.non_existent_user")
        expected = "The requested profile does not exist."
        self.assertTrue(response.data['errors']['detail'] == expected)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    # followers status and followers list unit tests
    def test_user_profile_displays_following_status(self):
        """ 
        Tests whether the user profile endpoint dispalys if I follow the user
        after authentication 
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # login jake
        response = self.login_user()
        token = response.data['token']
        self.follow_user(token,"jakerrrrrr")
        response = self.get_profile_with_authentication(token,"jakerrrrrr")
        self.assertTrue(response.data['following'])
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_profile_following_is_false_without_authentication(self):
        """ 
        Tests whether the user profile endpoint following status returns false
        if I, the user is not authenticated
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # login jake
        response = self.login_user()
        token = response.data['token']
        self.follow_user(token,"jakerrrrrr")
        # get profile without token
        response = self.get_profile("jakerrrrrr")
        self.assertFalse(response.data['following'])
        self.assertEquals(status.HTTP_200_OK, response.status_code)
    
    def test_display_followers(self):
        """ 
        Tests whether all the followers of a user can be displayed
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # username -> jakerrrrrrrrr
        self.register_user_2()
        
        #jakerrrrrr logs in and follows jake
        response = self.login_user_1()
        token = response.data['token']
        self.follow_user(token,"jake")

        #jakerrrrrrrrr logs in and follows jake
        response = self.login_user_2()
        token = response.data['token']
        self.follow_user(token,"jake")

        response = self.list_followers(token,"jake")
        self.assertTrue(len(response.data['followers'])== 2)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_display_followers_without_authentication(self):
        """ 
        Tests whether all the followers of a user cant be displayed unless a
        token header is provided
        """
        token = ''
        response = self.list_followers(token,"jake")
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_display_followers_for_non_existent_profile(self):
        """ 
        Tests whether all the followers of a non_existent user cant be displayed 
        unless a token header is provided
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.list_followers(token,"non_existent_user")
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_display_following(self):
        """ 
        Tests whether all the profiles a user is following can be displayed
        """
        # username -> jake
        self.register_user()
        # username -> jakerrrrrr
        self.register_user_1()
        # username -> jakerrrrrrrrr
        self.register_user_2()
        
        #jake logs in and follows jakerrrrrr & jakerrrrrrrrr
        response = self.login_user()
        token = response.data['token']
        self.follow_user(token,"jakerrrrrr")
        self.follow_user(token,"jakerrrrrrrrr")

        response = self.list_following(token,"jake")
        self.assertTrue(len(response.data['followers'])== 2)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_display_following_without_authentication(self):
        """ 
        Tests whether all the profiles a user is following cant be displayed
        unless a token header is provided
        """
        token = ''
        response = self.list_following(token,"jake")
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_display_following_for_non_existent_profile(self):
        """ 
        Tests non-existent profile cant display `following` list
        """
        self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.list_following(token,"non_existent_user")
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    