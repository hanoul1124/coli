from bigchaindb_driver.crypto import generate_keypair
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .forms import LoginForm, SignupForm
from .models import User
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
        birthdate = request.POST['birthdate']
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
