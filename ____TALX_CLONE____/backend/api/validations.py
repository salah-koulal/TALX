#backend/api/validations.py

from django.core.exceptions import ValidationError
from .models import Users


def custom_validation(data):
    email = data["email"].strip()
    username = data["username"].strip()
    password = data["password"].strip()
    ##
    if not email or Users.objects.filter(email=email).exists():
        raise ValidationError("choose another email")
    ##
    if not username or Users.objects.filter(username=username).exists():
        raise ValidationError("choose another username")
    ##

    if not password or len(password) < 8:
        raise ValidationError("choose another password, min 8 characters")
    ##
    if not username:
        raise ValidationError("choose another username")
    return data


def validate_email(data):
    email = data["email"].strip()
    if not email:
        raise ValidationError("an email is needed")
    return True


def validate_username(data):
    username = data["username"].strip()
    if not username:
        raise ValidationError("choose another username")
    return True


def validate_password(data):
    password = data["password"].strip()
    if not password:
        raise ValidationError("a password is needed")
    return True