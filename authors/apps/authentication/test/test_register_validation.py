from .base import BaseTest
from django.urls import reverse


class UserAuthenticationTestCase(BaseTest):

    def user_credentials(self, email, username, password):
        """Returns user credentials in correct format"""
        credentials = {
            "user": {
                "email": email,
                "username": username,
                "password": password
            }
        }
        return credentials

    def test_if_email_field_is_empty(self):
        """Test if the email field is empty"""

        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('', 'Taps', 'Pass1234@#'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['email'][0],
                         "Email field is required.")

    def test_if_email_is_available(self):
        """Test is the email is available"""
        self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', 'HelloWorldKen12!3'),
            format='json'
        )

        response = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake2', 'HelloWorldKen12!3'),
            format='json'
        )
        self.assertEqual(response.data['errors']['email'][0],
                         "This email is not available. Please try another.")

    def test_if_email_is_valid(self):
        """Test if the email address is valid"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@gmail', 'jake2', 'HelloWorldKen12!3'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['email'][0],
                         "Enter a valid email address.")

    def test_if_username_field_is_empty(self):
        """Test if the username field is empty"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', '', 'HelloWorldKen12!3'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['username'][0],
                         "Username field is required.")

    def test_if_username_is_available(self):
        """Test if the username is available"""
        self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', 'HelloWorldKen12!3'),
            format='json'
        )

        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake2@jake.jake', 'jake', 'HelloWorldKen12!3'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['username'][0],
                         "This username is not available. Please try another.")

    def test_if_password_field_is_empty(self):
        """Test if the password field is empty"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', ''),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['password'][0],
                         "Password field is required.")

    def test_if_password_is_valid_length(self):
        """Test if the password is of valid length"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', 'Hel12!3'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['password'][0],
                         "Create a password at least 8 characters.")

    def test_if_password_has_a_number(self):
        """Test if the password has a number"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', 'HelloWorldKen!'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['password'][0],
                         "Create a password with at least one number.")

    def test_if_password_has_an_uppercase_letter(self):
        """Test if the password is of valid length"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('jake@jake.jake', 'jake', 'helloworldken12!3'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['password'][0],
                         "Create a password with at least one uppercase letter")

    def test_if_password_has_a_special_character(self):
        """Test if the password is of valid length"""
        test_data = self.client.post(
            reverse('authentication:user_signup'),
            self.user_credentials('esther@jake.jake', 'esther', 'Helloworldken123'),
            format='json'
        )
        self.assertEqual(test_data.data['errors']['password'][0],
                         "Create a password with at least one special character.")