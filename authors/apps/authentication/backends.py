import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
   '''
   By subclassing Django BaseAuthentication
   we are able able to override authenticate()
   and define ours
   '''

   authentication_header_prefix = 'Bearer'

   def authenticate(self, request):
       """
       Authenticates a user by generating a jwt token.
       The user uses the token to access resources that need an acess token.
       JWT token has become a defacto standard for authentication
       """
       request.user = None


       # `header` array has the prefix(Access_token) and the JWT Token
       # that has to be checked for validity
       token_header = authentication.get_authorization_header(request).split()

       token_header_prefix = self.authentication_header_prefix.lower()

       if not token_header:
           return None

       if len(token_header) != 2:
           # Invalid token header. Only prefix provided probably.
           # Token missing. Should not be authenticated.
           return None

       # JWT token has to be decoded to get individual components (prefix, token).

       prefix = token_header[0].decode('utf-8') # The prefix.

       current_token = token_header[1].decode('utf-8') # The token string.

       if prefix.lower() != token_header_prefix:

           # Make a comparison between prefix after decoding and the expected.
           # A mismatch means not authenticated.
           return None

       # Otherwise call private method passing the token and user.

       return self._authenticate_credentials(request, current_token)

   def _authenticate_credentials(self, request, token):
       """
        Private method tries to authenticate a user based on token provided.
        Returns a jwt token and a user if successful.
       """
       try:
           payload = jwt.decode(token, settings.SECRET_KEY)
       except:
           msg = 'Invalid token. Could not decode token. Possibly Damaged.'
           raise exceptions.AuthenticationFailed(msg)

       try:
           user = User.objects.get(pk=payload['id'])
       except user.DoesNotExist:
           msg = 'Token did not match any user..'
           raise exceptions.AuthenticationFailed(msg)

       if not user.is_active:
           msg = 'This user is in_active.'
           raise exceptions.AuthenticationFailed(msg)
       return (user, token)