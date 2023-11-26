from django.contrib.auth.hashers import make_password
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from users.models import User
from users.tokens import get_tokens_for_user


def oauth2_sign_in(token):
    try:
        response = id_token.verify_oauth2_token(token, requests.Request())
        email = response.get('email')
        password = make_password(email.split('@')[0])
        first_name = response.get('given_name')
        last_name = response.get('family_name')
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password)
        return get_tokens_for_user(user)
    except ValueError:
        raise AuthenticationFailed('Bad token Google', status.HTTP_403_FORBIDDEN)