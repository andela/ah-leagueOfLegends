'''
Notification tests
'''
from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status

class NotificationTestCase(BaseTest):
    '''
    notifications tests
    '''
    comment = {
        "comment": {
            "body": "I do believe"
        }
    }
    user1 = {
            "user": {
                "email": "jake@jakerr.jake",
                "username": "Eddy",
                "password": "J!ake123456"
            }
        }
    user2 = {
        "user": {
            "email": "jason@gmail.jake",
            "username": "jason",
            "password": "J!ake123456"
        }
    }
    user3 = {
        "user": {
            "email": "mercy@gmail.com",
            "username": "mercy",
            "password": "J!ake123456"
        }
    }
    user4 = {
        "user": {
            "email": "Loice@gmail.com",
            "username": "loice",
            "password": "J!ake123456"
        }
    }

    def get_user1_token(self):
        '''
        returns token to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user1,
            format='json')
        token = response.data['token']
        return token

    def get_user2_token(self):
        '''
        Returns token for 2nd user to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user2,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user2,
            format='json')
        token = response.data['token']
        return token

    def get_user3_token(self):
        '''
        Returns token for 3rd user to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user3,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user3,
            format='json')
        token = response.data['token']
        return token

    def get_user4_token(self):
        '''
        Returns token for 4th user to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user4,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user4,
            format='json')
        token = response.data['token']
        return token

    def create_article(self):
        '''
        create article
        '''
        article = {
            "article": {
                "title": "test article",
                "description": "Best believe",
                "body": "It really is"
            }
        }
        token = self.get_user1_token()
        return self.client.post(
            '/api/articles',
            article,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        

    def test_notification_sent_after_article_creation(self):
        '''
        Test that a notification is sent to users after an articel is created
        '''
        user1_token = self.get_user1_token()
        user2_token = self.get_user2_token()
        res = self.client.put(
            '/api/profiles/Eddy/follow',
            HTTP_AUTHORIZATION='Bearer ' + user2_token,
        )
        resp = self.client.get(
            '/api/Eddy/followers',
            HTTP_AUTHORIZATION='Bearer ' + user1_token,

            format='json'
        )
        self.create_article()
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user2_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_get_single_notification(self):
        user1_token = self.get_user1_token()
        user2_token = self.get_user2_token()
        res = self.client.put(
            '/api/profiles/Eddy/follow',
            HTTP_AUTHORIZATION='Bearer ' + user2_token,
        )
        resp = self.client.get(
            '/api/Eddy/followers',
            HTTP_AUTHORIZATION='Bearer ' + user1_token,

            format='json'
        )
        self.create_article()
        response = self.client.get(
            '/api/notifications/1',
            HTTP_AUTHORIZATION='Bearer ' + user2_token,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        

    def test_notification_not_sent_to_non_followers(self):
        '''
        test notifications for article creation should only be sent to followers
        '''
        user1_token = self.get_user1_token()
        user2_token = self.get_user2_token()
        user3_token = self.get_user3_token()
        res = self.client.put(
            '/api/profiles/Eddy/follow',
            HTTP_AUTHORIZATION='Bearer ' + user2_token,
        )
        resp = self.client.get(
            '/api/Eddy/followers',
            HTTP_AUTHORIZATION='Bearer ' + user1_token,

            format='json'
        )
        self.create_article()
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user3_token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)


    def test_notification_sent_after_comment(self):
        '''
        Test notitification sent after article is favorited
        '''
        user_1 = self.get_user1_token()
        user_2 = self.get_user2_token()
        user_3 = self.get_user3_token()
        article = self.create_article()
        slug = article.data.get("slug")
        self.client.post(
            '/api/articles/'+slug+'/favorite',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        res = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + user_3,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_notification_sent_only_to_users_who_faved_the_article(self):
        '''
        notifications should only be sent to users who favorited the article
        '''
        user_1 = self.get_user1_token()
        user_2 = self.get_user2_token()
        user_3 = self.get_user3_token()
        user_4 = self.get_user4_token()
        article = self.create_article()
        slug = article.data.get("slug")
        self.client.post(
            '/api/articles/'+slug+'/favorite',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        res = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + user_3,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_4,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    def test_notification_not_sent_to_unsubscribed_users(self):
        '''
        notifications should only be sent to subscribed users
        '''
        user_1 = self.get_user1_token()
        user_2 = self.get_user2_token()
        user_3 = self.get_user3_token()
        article = self.create_article()
        slug = article.data.get("slug")
        self.client.post(
            '/api/articles/'+slug+'/favorite',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        self.client.put(
            '/api/notifications/unsubscribe',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        res = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + user_3,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)


    def test_user_can_subscribe_and_unsubscribe(self):
        '''
        users should be able to subscribe and unsubscribe to notifications
        '''
        user_1 = self.get_user1_token()
        user_2 = self.get_user2_token()
        user_3 = self.get_user3_token()
        article = self.create_article()
        slug = article.data.get("slug")
        self.client.post(
            '/api/articles/'+slug+'/favorite',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        self.client.put(
            '/api/notifications/unsubscribe',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        res = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + user_3,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)
        self.client.put(
            '/api/notifications/subscribe',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
            format='json'
        )
        res = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + user_3,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

        
