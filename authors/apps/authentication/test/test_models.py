from django.test import TestCase
from ..models import User


class UserTest(TestCase):
    def setUp(self):
        User.objects.create_user("author", "author.me@gmail.com", "letmein")
        User.objects.create_superuser("admin", "admin.author@gmail.com", "letmein")

    def test_user_name(self):
        user1 = User.objects.get(username="author")
        self.assertEqual(user1.email, "author.me@gmail.com")
        self.assertEqual(user1.get_full_name, "author")
        self.assertEqual(user1.get_short_name(), "author")

    def test_superuser(self):
        user2 = User.objects.get(username="admin")
        self.assertEqual(user2.email, "admin.author@gmail.com")
        self.assertTrue(user2.is_superuser)
