from bigchaindb_driver import BigchainDB
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

    # 해당 로그인 유저가 가진 public key를 블록체인 DB상의 metadata에서 검색한다
    # Asset의 트랜잭션 metadata에는 항상 현재 소유자 public key를 기록할 것
    # 확인 후 metadata 중 해당 public key가 존재한다면 해당 유저가 등록한 DID가 있다는 뜻
    # True/False를 리턴한다
    @property
    def have_asset(self):
        db = BigchainDB('https://test.ipdb.io/')
        if db.metadata.get(search=self.public_key):
            return True
        else:
            return False


# 복수의 PID를 가질 수 있으므로, Foreign Key를 사용하는 방식을 채택
class LatestTransaction(models.Model):
    # 어떤 유저의 최신 트랜잭션인지
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    # 보유 Asset의 트랜잭션 ID(가장 최신)
    asset_id = models.CharField(max_length=150, blank=True, null=True)
    # 해당 유저의 몇 번째 Asset에 대한 트랜잭션인지(same with 'pet_entry')
    entry_num = models.PositiveSmallIntegerField(blank=True, null=True)
    # 해당 트랜잭션이 현재 상대의 서명이 완료된 상태인지
    # 가령, 수의사가 진단 자료를 작성 중인 경우, 유저로부터 펫 소유권을 일시적으로 TRASNFER 받음
    # 이후 수의사가 진단 자료를 작성해 Asset data가 추가된 상태로
    # 본래 유저에게 TRANSFER를 요청하여, 유저가 private key로 이를 서명
    # 유저가 반환 받아 서명하기 전까지는 비활성화 상태(=승인 대기중)
    is_active = models.BooleanField(default=True, blank=True)
