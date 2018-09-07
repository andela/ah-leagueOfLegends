
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


    def update_article(self, token, slug, article):

        """Helper method to update an article"""
        return self.client.put(
            '/api/articles/' + slug,
            article,
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )

    def delete_article(self, token, slug):

        """Helper method to delete an article"""
        
        return self.client.delete(
            '/api/articles/' + slug,
            HTTP_AUTHORIZATION='Bearer ' + token,
        )


    def test_create_successfully(self):


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

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_create_article_with_fake_token(self):

        response = self.client.post(
               self.SIGN_UP_URL,
               self.user_cred,
               format='json')
        response = self.client.post(
               reverse('authentication:user_login'),
               self.user_cred,
               format='json')
        token =  'hgbbbjbhhjknkj'

        article= {
                    "article": 
                      {
                      "title": "How to feed your dragon",
                      "description": "Wanna know how?",
                      "body": "You don't believe?",
                        }
                  }

        response = self.create_article(token, article)

        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_article_with_empty_data(self):

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
                      "title": "",
                      "description": "",
                      "body": "",
                        }
                  }

        response = self.create_article(token, article)

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_any_user_can_get_articles(self):
        """
        Tests that any user whether authenticated or not can get a list of
        all articles
        """

        response = self.client.get('/api/articles')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        response = self.client.get('/api/articles')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_unverified_user_cannot_create_article(self):
        """
        Test that a user without an account cannot create an article
        """
        response = self.client.post(
               self.SIGN_UP_URL,
               self.user_cred_wrong_pass,
               format='json')
        response = self.client.post(
               reverse('authentication:user_login'),
               self.user_cred_wrong_pass,
               format='json')
        # fake token because user is not verified
        token = 'gv jkknk m lk'

        article= {
                    "article": 
                      {
                      "title": "How to feed your dragon",
                      "description": "Wanna know how?",
                      "body": "You don't believe?",
                        }
                  }

        response = self.create_article(token, article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_update_article_successfully(self):

        """ Tests whether a user can update an article
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
        response = self.create_article(token, self.testArticle)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # Update the created article
        response = self.update_article(
            token, 'how-to-feed-your-dragon', self.testArticle1)
        self.assertIn('how-to-train-your-dragon', response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_article_successfully(self):

        """ Tests whether a user can update an article
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
        response = self.create_article(token, self.testArticle)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # Update the created article
        response = self.delete_article(token, 'how-to-feed-your-dragon')
        response = self.client.get('/api/articles/how-to-feed-your-dragon')
        self.assertEqual(response.status_code, 
            status.HTTP_404_NOT_FOUND)

    def test_user_delete_article_not_author(self):

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

        article= {
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
        response = self.delete_article(token, 'how-to-feed-your-dragon')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    def test_user_update_article_not_author(self):

        """ Tests whether a user can update an article when not author
        Method registers a user, logs in the user,
        creates an article, then logs in another,
        and tries to update the article
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
        # Assert true that an article has been created
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
        # Update the article created by another user.
        # Expects to throw a 404 error
        response = self.update_article(
            token, 'how-to-feed-your-dragon', self.testArticle1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update_article_not_found(self):

        """ Tests whether a user can update an article when not author
        Method registers a user, logs in the user,
        creates an article, then logs in another,
        and tries to update the article
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
        # Assert true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED, 
            response.status_code)

        # Update the article created by another user.
        # Expects to throw a 404 error
        response = self.update_article(
            token, 'how-to-feed-your-dragonn', self.testArticle1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_article_not_found(self):

        """ Tests whether a user can update an article when not author
        Method registers a user, logs in the user,
        creates an article, then logs in another,
        and tries to update the article
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
        # Assert true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED, 
            response.status_code)

        # Update the article created by another user.
        # Expects to throw a 404 error

        response = self.delete_article(token, 'how-to-feed-your-dragonn')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_article_already_deleted(self):

        """ Tests whether a user can update an article when not author
        Method registers a user, logs in the user,
        creates an article, then deletes,
        and tries to delete the article again

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
        # Assert true that an article has been created
        self.assertEquals(status.HTTP_201_CREATED, 
            response.status_code)

        # Update the article created by another user.
        # Expects success 200 OK
        response = self.delete_article(token, 'how-to-feed-your-dragon')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Try to delete an already deleted article, expects a 404_NOT_FOUND

        response = self.delete_article(token, 'how-to-feed-your-dragon')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


