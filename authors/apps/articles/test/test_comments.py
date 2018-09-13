'''
Article tests
'''
from authors.apps.base_test import BaseTest
from django.urls import reverse
from rest_framework.views import status
import json
from .test_articles import ArticleTestCase

class CommentTestCase(BaseTest):
    '''
    Comment Test Class, Inherits from Basetest
    '''
    article = {
        "article": {
            "title": "test article",
            "description": "Best believe",
            "body": "It really is"
        }
    }
    article2 = {
        "article": {
            "title": "test article two",
            "description": "Best believe",
            "body": "It really is"
        }
    }
    comment = {
        "comment": {
            "body": "I do believe"
        }
    }
    empty_comment = {
        "comment": {
            "body": " "
        }
    }


    def get_token(self):
        response = self.client.post(
            self.SIGN_UP_URL,
            self.user_cred,
            format='json')
        response = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = response.data['token']
        return token

    def get_user2_token(self):
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


    def create_comment(self,comment):
        """
        Helper method to creates an article
        """
        token = self.get_token()
        self.client.post(
            '/api/articles',
            self.article,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        return self.client.post(
            '/api/articles/test-article/comments',
            comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )

    def test_add_comments(self):

        response = self.create_comment(self.comment)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_comment_on_non_existent_article(self):
        '''
        test that it throws a 404 error
        '''
        token = self.get_token()
        response = self.client.post(
            '/api/articles/not-found/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_comment(self):
        '''
        Test it throws 400 error if comment body is empty
        '''
        token = self.get_token()
        self.client.post(
            '/api/articles',
            self.article,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response = self.client.post(
            '/api/articles/test-article/comments',
            self.empty_comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_get_comments(self):
        '''
        test user can get all comments to an article
        '''
        self.create_comment(self.comment)
        response = self.client.get(
            '/api/articles/test-article/comments'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_comments_for_non_existant_article(self):
        response = self.client.get(
            '/api/articles/test-article-wrong/comments'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_comments(self):
        '''
        test that user can get single comment
        '''
        response = self.create_comment(self.comment)
        article_id = response.data["id"]
        response = self.client.get(
            '/api/articles/test-article/comments/'+str(article_id)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existent_comment(self):
        '''
        test that throws 404 error if comment does not exist
        '''
        response = self.client.get(
            '/api/articles/test-article/comments/500'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_wrong_id(self):
        '''
        test that user can delete comment
        '''
        token = self.get_token()
        self.client.post(
            '/api/articles',
            self.article2,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response = self.client.post(
            '/api/articles/test-article-two/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response1 = self.client.get('/api/articles/test-article-two/comments')
        response = self.client.delete(
            '/api/articles/test-article-two/comments/1',
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_comment_correct_id(self):
        '''
        Test that user can delete comment with right id
        '''
        token = self.get_token()
        self.client.post(
            '/api/articles',
            self.article2,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response = self.client.post(
            '/api/articles/test-article-two/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        article_id = response.data["id"]
        response = self.client.delete(
            '/api/articles/test-article-two/comments/'+ str(article_id),
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_non_owner_delete_article(self):
        '''
        Test that user can delete only their comments
        '''
        token = self.get_token()
        token2 = self.get_user2_token()
        self.client.post(
            '/api/articles',
            self.article2,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        response = self.client.post(
            '/api/articles/test-article-two/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        article_id = response.data["id"]
        response = self.client.delete(
            '/api/articles/test-article-two/comments/'+str(article_id),
            HTTP_AUTHORIZATION='Bearer ' + token2
        )
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
