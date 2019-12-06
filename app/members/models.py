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
    # 이후 Blockchain DB에서 사용 및 저장될 유저의 Public Key를 저장하는 공간
    # 최초 유저 생성 시에는 비어있는 상태로 시작(회원가입시에도 표기하지 않는 정보)
    # 이후 Generate_key()를 실행하면서 Public Key는 저장되고, Private Key는 유저 로컬 공간에 다운로드되도록 만든다.
    # 모바일 어플리케이션이라면 Private Key의 로컬 저장 및 재사용이 매우 쉬울 것이나,
    # 웹 기반에서는 유저가 직접 Private Key File을 업로드하도록 만들어야 한다
    public_key = models.CharField(
        'Public Key',
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )