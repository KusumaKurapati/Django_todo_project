import jwt
import hashlib
import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.datetime.utcnow(),
        'type': 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            payload = decode_jwt(token)
            if payload.get('type') != 'access':
                raise AuthenticationFailed('Invalid token type')

            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except AuthenticationFailed:
            raise



