import json
from builtins import super

from rest_framework.renderers import JSONRenderer
from .token_gen import generate_token


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
       # If the view throws an error (such as the user can't be authenticated
       # or something similar), `data` may or may not contain an `errors` key.
       #  We want the default JSONRenderer to handle rendering errors,
       # so we need to check for this case.

       # checks for the 'detail' key from the data given, then checks for
       # the 'errors' key. If both are not found then errors is set to None
       errors = data.get('detail') \
           if data.get('detail', None) is not None \
           else data.get('errors', None)
       if errors is not None:
           # As mentioned about, we will let the default JSONRenderer handle
           # rendering errors.
           from rest_framework.utils.serializer_helpers import ReturnDict
           if isinstance(errors, ReturnDict):
               # if the specifies error is found in our dict of errors it will be used in the response
               return super(UserJSONRenderer, self).render(data)
           else:
               # error not found and therefor will be added
               errors = dict(errors=dict(detail=errors))
               return super(UserJSONRenderer, self).render(errors)

       token = generate_token(data)
       data['token'] = token
       # Finally, we can render our data under the "user" namespace.
       return json.dumps({'user': data})