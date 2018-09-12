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


    def test_search_article_by_title_successfully(self):
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
        response = self.client.get('/api/search/articles?title=dragon')


        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_search_article_by_tag_successfully(self):
        """ 
        Test an article can be searched by title and returned 
        successfully

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
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }
                }

        
        response = self.create_article(token, article)
        response = self.client.get('/api/search/articles?tagList=reactjs')


        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_search_article_by_author_successfully(self):
        """ 
        Test an article can be searched by author
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
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }
                }

        
        response = self.create_article(token, article)
        response = self.client.get('/api/search/articles?search=jake')


        self.assertEquals(status.HTTP_200_OK, response.status_code)


    def test_search_article_by_author_not_found(self):
        """ 
        Test an article can be searched by title not found
        Count and results should be zero and empty respectively

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
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }
                }

        
        response = self.create_article(token, article)
        response = self.client.get('/api/search/articles?search=jakeee')
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
        self.assertEquals(status.HTTP_200_OK, response.status_code)


    def test_search_article_by_title_not_found(self):
        """ 
        Test an article can be searched by title not found
        Count and results should be zero and empty respectively

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
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }
                }

        
        response = self.create_article(token, article)
        response = self.client.get('/api/search/articles?title=dragonnn')
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_search_article_by_tag_not_found(self):
        """ 
        Test an article can be searched by title not found
        Count and results should be zero and empty respectively

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
                            "title": "How to train your dragon",
                            "description": "Ever wonder how?",
                            "body": "You have to believe",
                            "tagList": ["reactjs", "angularjs", "dragons"]
                        }
                }

        
        response = self.create_article(token, article)
        response = self.client.get('/api/search/articles?tagList=dragonnn')
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
        self.assertEquals(status.HTTP_200_OK, response.status_code)