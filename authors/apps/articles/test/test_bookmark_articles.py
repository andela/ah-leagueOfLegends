from .test_articles import ArticleTestCase
from django.urls import reverse
from rest_framework.views import status


class BookmarkArticleTestCase(ArticleTestCase):
    """Tests Bookmark articles views"""
    article = {
        "article":
            {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"],
            }
    }

    def test_if_user_can_bookmark_without_authentication(self):
        """Test if user can bookmark article without authentication"""
        # Bookmark an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/bookmark/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_if_user_can_bookmark_unexisting_article(self):
        """Test if the user can bookmark an article that does not exist"""
        # Register user
        self.register_user()
        # Login user
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        # Create token
        token = res.data['token']
        # Bookmark an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/bookmark/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_user_can_add_bookmark(self):
        """Test if user can add a bookmark"""
        # Register user
        self.register_user()
        # Login user
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        # Create token
        token = res.data['token']
        # Create article
        response = self.create_article(token, self.article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # Bookmark an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/bookmark/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_if_user_can_remove_bookmark(self):
        """Test if user can add a bookmark"""
        # Register user
        self.register_user()
        # Login user
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        # Create token
        token = res.data['token']
        # Create article
        response = self.create_article(token, self.article)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        # Bookmark an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/bookmark/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Remove bookmark from an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/bookmark/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
