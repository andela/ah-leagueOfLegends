from .test_articles import ArticleTestCase
from django.urls import reverse
from rest_framework.views import status


class ReportArticleTestCase(ArticleTestCase):
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

    def test_if_user_can_report_without_authentication(self):
        """Test if user can report an article without authentication"""

        response = self.client.put(path='/api/articles/how-to-train-your-dragon/report')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_if_none_admin_user_can_get_reports(self):
        self.register_user()
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = res.data['token']
        response = self.client.get(path='/api/articles/how-to-your-dragon/reports',
                                   HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_can_report_articles(self):
        self.register_user()
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = res.data['token']
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
        data = {"report": {"body": "A lot of plagiarism"}}
        response = self.client.post(path='/api/articles/how-to-feed-your-dragon/report', data=data,
                                    HTTP_AUTHORIZATION='Bearer ' + token, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_user_can_report_articles_without_body(self):
        self.register_user()
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = res.data['token']
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
        response = self.client.post(path='/api/articles/how-to-feed-your-dragon/report',
                                    HTTP_AUTHORIZATION='Bearer ' + token, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_user_can_report_missing_article(self):
        self.register_user()
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = res.data['token']
        response = self.client.post(path='/api/articles/how-to-your-dragon/report',
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['detail'], 'An article with that slug does not exist')

    def test_if_admin_can_list_reports(self):
        self.register_user()
        res = self.client.post(
            reverse('authentication:user_login'),
            self.user_cred,
            format='json')
        token = res.data['token']
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
        data = {"report": {"body": "A lot of plagiarism"}}
        response = self.client.post(path='/api/articles/how-to-feed-your-dragon/report', data=data,
                                    HTTP_AUTHORIZATION='Bearer ' + token, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "user": {
                "username": "Teddy",
                "email": "teddykavooh@gmail.com",
                "password": "HelloWorldKen12!3",
                "is_superuser": True
            }
        }
        response = self.client.post(path='/api/users/', data=data,
                                    format='json')
        print(response.data)
        data = {"user": {"email": "teddykavooh@gmail.com", "password": "HelloWorldKen12!3"}
                }
        response = self.client.post(path='/api/users/login/', data=data,
                                    format='json')
        token = response.data['token']
        response = self.client.get(path='/api/articles/how-to-feed-your-dragon/reports',
                                   HTTP_AUTHORIZATION='Bearer ' + token, format='json')
        print(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
