from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
import datetime


# Create your models here.
class PhoneNumbervalidator(validators.RegexValidator):
    regex = '[0-9]+'
    message = 'Enter a valid phone number. This value may contains only numbers without "-"'


class User(AbstractUser):
    SEX = (('male', 'Male'), ('female', 'Female'))
    sex = models.CharField(max_length=6, choices=SEX, default='male')
    birthdate = models.DateField(default=datetime.date(1990,1,1))
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
    AUTHORITIES = (
        ('Owner', 'Pet Owner'),
        ('Vet', 'Veterinarian'),
        ('Comp', 'Company')
    )
    authority = models.CharField(
        max_length=5,
        choices=AUTHORITIES,
        default='Owner'
    )