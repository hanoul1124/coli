from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


# Create your models here.
class PhoneNumbervalidator(validators.RegexValidator):
    regex = '[0-9]+'
    message = 'Enter a valid phone number. This value may contains only numbers without "-"'


class User(AbstractUser):

    phone_number_validator = PhoneNumbervalidator()
    phone_number = models.CharField(
        'Phone Number',
        max_length=20,
        unique=True,
        validators=[phone_number_validator],
        error_messages={
            'unique': 'A User with that Phone Number already exists'
        },
    )