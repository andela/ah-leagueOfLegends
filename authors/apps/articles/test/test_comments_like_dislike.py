from authors.apps.base_test import BaseTest
from django.urls import reverse
from authors.apps.articles.models import Article
from rest_framework.views import status
import json


class CommentsLikeDislikeTestCase(BaseTest):
    """ 
    Class implements tests for liking and disliking comments.
    """
    article = {
        "article": {
            "title": "test article",
            "description": "Best believe",
            "body": "It really is"
        }
    }

    comment = {
        "comment": {
            "body": "Wagwan"
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

    def create_comment(self, token, slug, comment):
        """
        Helper method to creates an article
        """
        self.client.post(
            '/api/articles',
            self.article,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )
        return self.client.post(
            '/api/articles/test-article/comments',
            self.comment,
            HTTP_AUTHORIZATION='Bearer ' + token,

            format='json'
        )

    def test_like_comment(self):
        """Test test the liking of a comment"""
        # created a user, logged in the user
        # Created a token
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }
        # created the article
        response = self.create_article(token, article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # creating a comment
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # like a comment
        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/'+str(comment_id)+'/like',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_dislike_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/'+str(comment_id)+'/dislike',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_unlike_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/'+str(comment_id)+'/like',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_undislike_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/'+str(comment_id)+'/dislike',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_like_missing_article(self):
        """Test test the liking of a comment"""
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        response = self.client.put('/api/articles/how-to-feed-your-drago/comments/' + str(comment_id) + '/dislike',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_like_missing_comment(self):
        """Test test the liking of a comment"""
        token = self.get_token()
        article = {
            "article":
                {
                    "title": "How to feed your dragon",
                    "description": "Wanna know how?",
                    "body": "You don't believe?",
                }
        }

        response = self.create_article(token, article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/99/dislike',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_like_comment_if_article_does_not_exist(self):
        """Test test the liking of a comment in an article that does not exist"""
        # created a user, logged in the user
        # Created a token
        token = self.get_token()
        slug = 'how-to-feed-your-dragon'
        comment = {
            "comment": {
                "body": "Wagwan"
            }
        }

        response = self.create_comment(token, slug, comment)
        comment_id = response.data["id"]
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # like a comment
        response = self.client.put('/api/articles/how-to-feed-your-dragon/comments/' + str(comment_id) + '/like',
                                   HTTP_AUTHORIZATION='Bearer ' + token,
                                   format='json'
                                   )
        self.assertEquals(response.data['detail'], 'An article with this slug does not exist.')
