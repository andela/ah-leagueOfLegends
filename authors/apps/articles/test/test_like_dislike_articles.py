from .test_articles import ArticleTestCase
from django.urls import reverse
from rest_framework.views import status


class DislikeLikeArticleTestCase(ArticleTestCase):
    """Tests Like and Dislike articles views"""

    article = {
        "article":
            {
                "author": "jake",
                "body": "It takes a Jacobian",
                "tagList": [
                    "dragons",
                    "training"
                ],
                "created_at_date": "2018-09-11T19:56:22.112185+00:00",
                "description": "Ever wonder how?",
                "slug": "how-to-train-your-dragon",
                "title": "How to train your dragon",
                "updated_at_date": "2018-09-11T19:56:22.112220+00:00",
                "like": 0,
                "dislike": 0
            }
    }

    def test_if_user_can_like_without_authentication(self):
        """Test if user can like article without authentication"""
        # Like an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_if_user_can_dislike_without_authentication(self):
        """Test if user can dislike article without authentication"""
        # Dislike an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_if_user_can_like_unexisting_article(self):
        """Test if the user can like an article that does not exist"""
        # Register user
        self.register_user()
        # Login user
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        # Create token
        token = res.data['token']
        # Like an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "The article does not exist.")

    def test_if_user_can_dislike_unexisting_article(self):
        """Test if the user can like an article that does not exist"""
        # Register user
        self.register_user()
        # Login user
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        # Create token
        token = res.data['token']
        # Dislike an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "The article does not exist.")

    def test_if_user_liking_is_successful(self):
        """Test if user liking is successful, if like does not exist"""
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
        # Like an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Added to Liked articles")

    def test_successful_article_disliking(self):
        """Test a successful disliking of an article"""
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
        # Dislike an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You Dislike this Article")

    def test_response_of_adding_a_like_after_adding_a_dislike(self):
        """Test the response of adding a like after adding a dislike"""
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
        # Dislike an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You Dislike this Article")
        # Like an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Removed from dislike and Added to Liked articles")

    def test_response_of_adding_a_dislike_after_adding_a_like(self):
        """Test the response of adding a dislike after adding a like """
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
        # Like an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Added to Liked articles")
        # Dislike an article
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Removed from Liked Articles and Added to Disliked articles")

    def test_response_of_double_liking(self):
        """Test the response of liking an article twice"""
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
        # Like an article, first request
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Added to Liked articles")
        # Like an article, second request
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/like/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You no longer like this article")

    def test_response_of_double_disliking(self):
        """Test the response of disliking an article twice"""
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
        # Dislike an article, first request
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You Dislike this Article")
        # Dislike an article, second request
        response = self.client.put(path='/api/articles/how-to-train-your-dragon/dislike/',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "You no longer dislike this article")
