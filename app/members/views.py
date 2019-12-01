from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import Http404
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

# def sign_up(request):
#     if request.method == 'POST':
#         id = request.POST['id']
#         pw = request.POST['pwd']
#         sex = request.POST['sex']
#         fullname = request.POST['name']
#         email = request.POST['email']
#         phone = request.POST['phonenumber']
#         birth_year = int(request.POST['birth_year'])
#         birth_month = int(request.POST['birth_month'])
#         birth_day = int(request.POST['birth_day'])
#         authority = request.POST['Authority']
#
#         try:
#             # User creation
#             obj = User.objects.create(
#                 username=id, sex=sex, full_name=fullname,
#                 email=email, phone_number=phone,
#                 birthday=datetime.date(birth_year, birth_month, birth_day),
#                 authority=authority
#             )
#             obj.set_password(pw)
#             obj.save()
#         except ValueError:
#             # ValueError exception: datetime.date error
#             return render(request, 'web/sign_up.html', {'signup_fail': True})
#         except ValidationError:
#             # ValidationError exception: phone number validation error
#             return render(request, 'web/sign_up.html', {'signup_fail': True})
#     else:
#         raise Http404("404 Not Found.")
#
#     return render(request, 'web/COLI_main.html', {'signup': True})
