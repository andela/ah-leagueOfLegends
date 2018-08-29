import jwt
import datetime
from django.conf import settings


def generate_token(credentials: dict, expiry: float = 76400):
    """Generates JWT Token using user payload data

    Arguments:
        credentials {dict} -- [Contains user payload data]

    Keyword Arguments:
        expiry {float} -- [Expiry time] (default: {76400})

    Returns:
        [type] -- [JWT Token]
    """

    payload = dict(
        identity=credentials,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry))
    return jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
