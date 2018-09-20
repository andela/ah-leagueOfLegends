from ..base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status
import json

class ArticleTestCase(BaseTest):
    """ 
    Class implements tests for artcles
    """
    
    def create_article(self, token, article):
        """
        Helper method to creates an article
        """
        return self.client.post(
            '/api/articles',
            article,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )


    def rate_article(self, token, slug, rate):
        """
        Helper method to creates an article
        """
        return self.client.post(
            '/api/articles/' + slug + '/rate/', rate,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )

    
    def test_cannot_rate_own_article(self):
        """ 
        Test an article can be searched by title
        and returned successfully

        """

        response = self.client.post(
               self.SIGN_UP_URL,
               self.user_cred,
               format='json')
        response = self.client.post(
               reverse('authentication:user_login'),
               self.user_cred,
               format='json')
        token = response.data['token']

        article= {
                    "article": 
                      {
                      "title": "How to feed your dragon",
                      "description": "Wanna know how?",
                      "body": "You don't believe?",
                        }
                  }
        
        response = self.create_article(token, article)
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 5
            }
            }
        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)


    def test_can_rate_article_successfully(self):
        """ Tests whether a user can delete an article when not author
        Method registers a user, logs in the user,
        creates an article, then updates the article
        """

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']

        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        # Asserr true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')

        token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 5
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

    def test_can_rate_article_more_than_once(self):
        """ Tests whether a user can delete an article when not author
        Method registers a user, logs in the user,
        creates an article, then updates the article
        """

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']

        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        # Asserr true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')

        token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 5
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)


       # token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 5
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED,
                          response.status_code)

    def test_can_rate_article_not_integer(self):
        """ Tests whether a user can delete an article when not author
        Method registers a user, logs in the user,
        creates an article, then updates the article
        """

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']

        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        # Asserr true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')

        token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": "5"
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED,
                          response.status_code)

    def test_can_rate_article_rate_value_greater_than_5(self):
        """ Tests whether a user can delete an article when not author
        Method registers a user, logs in the user,
        creates an article, then updates the article
        """

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']

        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        # Asserr true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')

        token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 6
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED,
                          response.status_code)

    def test_can_rate_article_rate_value_less_than_1(self):
        """ Tests whether a user can delete an article when not author
        Method registers a user, logs in the user,
        creates an article, then updates the article
        """

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']

        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        # Asserr true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED,
                          response.status_code)

        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred1,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred1,
            format='json')

        token = response.data['token']
        # Delete the article created by another user.
        # Expects to throw a 404 error
        slug = 'how-to-feed-your-dragon'
        rate={
            "rate": {
                "rating": 0
            }
            }

        response = self.rate_article(token, slug, rate)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED,
                          response.status_code)