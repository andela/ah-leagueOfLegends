# import jwt

# from django.conf import settings

from rest_framework import authentication, exceptions

# from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.TokenAuthentication):
    """This extends TokenAuthentication Class in the authentication class
       to enable creation of tokens

    Arguments:
        Authorization: Token 19401f7ac837da42b97f613d789819ff93537bee6a29
    """
    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
            from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        """Gets the authentication Header from the request and checks if the
           keywords are the same
        """

        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode:
            return None
        if len(auth) == 1:
            message = 'Invalid Token Header.No credentials provided'
            return exceptions.AuthenticationFailed(message)
        try:
            token = auth[1].decode()
        except UnicodeError:
            message = 'Invalid token header. Token string should not \
                       contain invalid characters.'
            raise exceptions.AuthenticationFailed(message)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            print(token)
            print(model)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Authentication Failed')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User Inactive or Deleted.')
        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
