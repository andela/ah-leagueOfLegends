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
    def get_user2_token(self):
        '''
        returns token to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')
        token = response.data['token']
        return token

    def get_user3_token(self):
        '''
        Returns token for 3rd user to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred2,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred2,
            format='json')
        token = response.data['token']
        return token

    def get_user4_token(self):
        '''
        Returns token for 3rd user to be used in tests
        '''
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred3,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred3,
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
        token = self.get_user2_token()
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
        signup = self.register_user()
        login = self.login_user()
        token = login.data.get('token')
        self.create_article()
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + token,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_notification_sent_after_comment(self):
        '''
        Test notitification sent after article is favorited
        '''
        signup = self.register_user()
        login = self.login_user()
        token = login.data.get('token')
        user_2 = self.get_user2_token()
        article = self.create_article()
        slug = article.data.get("slug")
        self.client.post(
            'api/articles/'+slug+'/favorites/',
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
        response = self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + user_2,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_notification_sent_only_to_users_who_faved_the_article(self):
        signup = self.register_user()
        login = self.login_user()
        article = self.create_article()
        slug = article.data.get("slug")
        token1 = login.data.get('token')
        token2 = self.get_user2_token()
        token3 = self.get_user3_token()
        token4 = self.get_user4_token()
        self.client.post(
            'api/articles/'+slug+'/favorites/',
            HTTP_AUTHORIZATION='Bearer ' + token1,
            format='json'
        )
        self.client.post(
            '/api/articles/'+slug+'/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token2,

            format='json'
        )
        response1 = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + token3,
        )
        response2 = self.client.get(
            '/api/notifications',
            HTTP_AUTHORIZATION='Bearer ' + token1,
        )
        self.assertEquals(len(response1.data), 0)
        self.assertEquals(len(response2.data), 1)

        

        
