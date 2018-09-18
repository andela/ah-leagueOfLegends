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
