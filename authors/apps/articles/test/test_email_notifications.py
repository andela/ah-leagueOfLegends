from django.core import mail
from authors.apps.articles.test.test_articles import ArticleTestCase


class EmailNotificationTestCase(ArticleTestCase):

    def test_sends_email_notification_on_article_created(self):
        response = self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.create_article(token, self.testArticle)
        self.assertEquals(len(mail.outbox), 2)

    def test_sends_email_notification_on_commented_articles(self):
        response = self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.create_article(token, self.testArticle)
        response = self.client.post(
                               '/api/articles/how-to-feed-your-dragon/comments',
                               {
                                   "comment": {"body": "Nice Article"}
                                }, format='json',
                               HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEquals(len(mail.outbox), 3)

    def test_user_unsubscribes_and_subscribes_to_email_notifications(self):
        response = self.register_user()
        response = self.login_user()
        token = response.data['token']
        response = self.client.put('/api/users/subscription/',
                                   HTTP_AUTHORIZATION='Bearer ' + token
                                   )
        expected = 'Successfully Unsubscribed'
        self.assertEquals(expected, response.data['message'])
        """Test user can subscribe back after subscribing.
        """
        response = self.client.put('/api/users/subscription/',
                                   HTTP_AUTHORIZATION='Bearer ' + token
                                   )
        expected = 'Successfully Subscribed'
        self.assertEquals(expected, response.data['message'])

