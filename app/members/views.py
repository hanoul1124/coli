import json

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .forms import LoginForm, SignupForm, CreatePIDForm
from .models import User, LatestTransaction
import datetime


# Create your views here.
# Function of login process
def login_view(request):
    context = {
        'form': LoginForm()
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')

        else:
            context['error'] = '잘못된 ID 혹은 Password를 입력하셨습니다.'
    return render(request, 'members/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main')


# Function of sign up process
def signup_view(request):
    context = {
        'form': SignupForm(),
    }

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        birthdate = datetime.datetime.strptime(request.POST['birthdate'], '%m/%d/%Y').strftime('%Y-%m-%d')
        sex = request.POST['sex']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        authority = request.POST['authority']

        if User.objects.filter(username=username).exists():
            context['error'] = f'사용자명({username})은 이미 사용중입니다.'
        elif password1 != password2:
            context['error'] = f'비밀번호와 비밀번화 확인란의 값이 일치하지 않습니다.'
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    last_name=last_name,
                    first_name=first_name,
                    birthdate=birthdate,
                    sex=sex,
                    email=email,
                    phone_number=phone_number,
                    authority=authority
                )
                login(request, user)
                return redirect('main')
            except ValueError:
                # ValueError exception: datetime.date error
                context["error"] = f'회원가입에 실패했습니다(부정확한 생년월일 기입)'
            except ValidationError:
                # ValidationError exception: phone number validation error
                context["error"] = f'회원가입에 실패했습니다(잘못된 휴대전화 번호 기입)'
    return render(request, 'members/signup.html', context)


# User Key Set generate and download private_key
def generate_user_key(request):
    # Blockchain keypair 생성
    user_keypair = generate_keypair()
    user = request.user
    user.public_key = user_keypair.public_key
    user.save()

    # User private key download
    filename = 'private_key.txt'
    response = HttpResponse(
        user_keypair.private_key, content_type='text/plain'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


# Pet Owner's Pet ID create
def create_pid(request):
    initial_data = {
        'pet_name': None,
        'pet_image': None,
        'pet_birthdate': None,
        'pet_breed': None,
        'pet_entry': None,
        'pet_noseprint': None,
        'owner_key': request.user.public_key,
        'owner_fingerprint': None,
        'vet': None,
        'private_key': None,
    }
    context = {
        'form': CreatePIDForm(initial=initial_data),
    }

    # if not POST(=GET), Render form itself
    # if POST, get Formdata and Make Transaction in Blockchain
    if request.method == 'POST':
        name = request.POST['pet_name']
        image = request.FILES['pet_image']
        birthdate = request.POST['pet_birthdate']
        breed = request.POST['pet_breed']
        entry = request.POST['pet_entry']
        noseprint = request.FILES['pet_noseprint']
        owner = request.POST['owner_key']
        fingerprint = request.FILES['owner_fingerprint']
        vet = request.POST['vet_key']
        private_key = request.POST['owner_private_key']

        # Local Default Storage에 저장 후 사용
        # 실제 서비스에서는 AWS S3를 사용 예정
        image_path = default_storage.save(
            f'{owner}/image.{image.content_type.split("/")[1]}',
            ContentFile(image.read())
        )

        noseprint_path = default_storage.save(
            f'{owner}/image.{noseprint.content_type.split("/")[1]}',
            ContentFile(noseprint.read())
        )

        fingerprint_path = default_storage.save(
            f'{owner}/image.{fingerprint.content_type.split("/")[1]}',
            ContentFile(fingerprint.read())
        )

        # 등록여부 검사 > 비문
        # 실제 서비스에서는 모든 비문의 메타데이터를 서버에서 관리할 것
        # On-chain에 저장하는 것이 아니라 효율을 위해 중앙화 서버에서 관리
        # 여기에서는 항상 Unique한 이미지가 들어오는 것으로 가정

        # PID Asset Data 정의
        PID_ASSET = {
            'data': {
                'pet_info': {
                    'pet_name': name,
                    'pet_image': image_path,
                    'pet_birth': birthdate,
                    'pet_breed': breed,
                    'pet_entry': entry,
                    'pet_noseprint': noseprint_path,
                    'owner': owner,
                    'owner_fingerprint': fingerprint_path
                },
                'pet_transactions': [
                    {
                        'transaction_num': 0,
                        'timestamp': json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str),
                        'agent': owner,
                        'transaction_type': 'CREATE',
                        # Vet 승인 시 Issue 확정
                        'content': f'PID Issue Application: {owner}',
                        # Vet 서명 이후 activated
                        'is_active': False
                    },
                ]
            }
        }

        # PID Metadata는 Vet이 승인한 이후에 생성

        # BigchainDB initailize
        db = BigchainDB('https://test.ipdb.io/')

        # prepare
        # 신청자 본인만 서명
        # Vet에게 소유권 제공 > Vet이 승인과 함께 다시 소유권 반환 > 발행 완료
        create_pid_prepare = db.transactions.prepare(
            operation='CREATE',
            signers=owner,
            # 승인 요청할 Vet
            recipients=vet,
            asset=PID_ASSET,
        )

        create_pid_fulfill = db.transactions.fulfill(
            create_pid_prepare,
            private_keys=private_key
        )

        create_pid_commit = db.transactions.send_commit(
            create_pid_fulfill
        )

        # 최신 트랜잭션 저장
        last_transaction = LatestTransaction.objects.create(
            user=request.user,
            asset_id=create_pid_fulfill['id'],
            entry_num=entry,
            is_active=False
        )
        last_transaction.save()

        return redirect('members:owners')
    return render(request, 'members/create_pid.html', context)


# Vet, Company User ID Create
def create_did(request):
    pass


# Owner 로그인 후 화면(PID 생성 진행 이후)
def owners_view(request):
    return render(request, 'members/owners.html')


# Asset Data 정의
# PID
# PID_ASSET = {
#     'data': {
#         'pet_info': {
#             # PET의 NAME
#             'pet_name': 'NAME',

#             # Pet 이미지 URL(호스팅 API)
#             'pet_image': 'PET_IMAGE_URL',

#             # Pet 생일
#             'pet_birth': 'PET_BIRTHDAY',

#             # Pet 품종
#             'pet_breed': 'PET_BREED',

#             # Pet 순서(해당 유저가 보유한 Pet중 등록 순서)
#             'pet_entry': 'PET_ENTRY_NUM',
#             # 구현 제외
#             # 'pet_parents': 'PET_PARENTS_ASSET_ID'

#             # Pet 비문 > IMAGE DATA 사용
#             # 비문 및 지분 데이터 이미지 모두 실제 사용에 있어서는 Storage(S3)를 사용
#             'pet_noseprint': 'NOSEPRINT',

#             # Owner
#             'owner': 'PUBLIC_KEY',

#             # Owner 지문 > IMAGE DATA 사용
#             'owner_fingerprint': 'FINGERPRINT'
#         },
#         'pet_transactions': [
#             # 아래와 같은 Pet Transaction이 매 행위(transaction 발생)마다 쌓이게 된다.
#             {
#                 # pet_transactions에 한 element가 추가될 때마다 num이 ++된다
#                 # 전체 pet_transaction 수. 최초 생성시 생성에 대한 transaction 기록 = 1
#                 'transaction_num': 'num++',
#                 # 해당 transaction이 이루어진 시간, updated_datetime
#                 'timestamp': 'datetime.now',
#                 # 해당 transaction을 수행한 사람의 public key
#                 'agent': 'agent_public_key',
#                 # 해당 transaction이 어떠한 기능을 수행하기 위한 것인지 설명
#                 # CREATE : 최초 생성 / ADD : 의료 정보 추가
#                 # EDIT : PET_INFO 정보 수정 / RETRIEVE : 펫 정보 조회(By Company)
#                 # NOTE : 수의사는 자신이 치료한 동물 한정으로 자료 조회 가능,
#                 #        오너는 항상 자신의 펫만 자료 조회 가능
#                 'transaction_type': 'CREATE|ADD|EDIT|RETRIEVE',
#                 # 진료 및 조회 내용
#                 'content': 'TEXT INPUT'
#             },
#         ]
#     }
# }
#
# PID_METADATA = {
#     # Owner
#     'owner': 'OWNER_PUBLIC_KEY',
#     # ID Type (Pet or VET/COMPANY)
#     'ID_Type': 'PID|DID',
#     # trasaction number(same with transaction num in Asset)
#     'transaction_num': 'num',
#     # 최초 CREATE시에만 적용, 최초 ID생성 일시
#     'date_created': 'datetime.date.today',
#     # 가장 최근의 Upade 일시(same with timestamp in Asset)
#     'date_updated': 'datetime.date.today'
# }
