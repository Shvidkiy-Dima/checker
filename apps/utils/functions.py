from typing import Optional
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from account.models import User


def is_valid_password(password: str, user: Optional[User] = None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``True, None``.
    If the password is invalid, return ``False, list_of_error_messages``.
    """
    try:
        validate_password(password, user)
    except ValidationError as e:
        return False, e.messages

    return True, None


def get_user_by_token(token):
    token = Token.objects.filter(key=token).first()
    return token.user if token else AnonymousUser()
