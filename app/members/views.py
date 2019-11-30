from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import User
import datetime

# Create your views here.
def main_page(request):
    return render(request, 'web/COLI_main.html', {})

def main_page2(request):
    return render(request, 'web/main2.html', {})

def main_page3(request):
    return render(request, 'web/main3.html', {})

def sign_in_page(request):
    return render(request, 'web/sign_in.html', {'error': False})

def sign_up_page(request):
    return render(request, 'web/sign_up.html', {})

# Function of login process
def login(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pwd1']
        try:
            # 아이디 검색
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            # 아이디가 존재하지 않습니다.
            return render(request, 'web/sign_in.html', {'error': True})

        if not user.check_password(pw):
            # 비밀번호가 일치하지 않습니다.
            return render(request, 'web/sign_in.html', {'error': True})
    else:
        raise Http404("404 Not Found.")

    return render(request, 'web/main_login.html', {})

# Function of sign up process
def sign_up(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pwd']
        sex = request.POST['sex']
        fullname = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        birth_year = request.POST['birth_year']
        birth_month = request.POST['birth_month']
        birth_day = request.POST['birth_day']
        authority = request.POST['Authority']

        try:
            obj = User.objects.create(username=id, password=pw, sex=sex,
            full_name=fullname, email=email, phone_number=phone,
            birthday=datetime.date(birth_year, birth_month, birth_day),
            authority=authority)
        except ValueError:
            return render(request, 'web/sign_up.html', {})
        except ValidationError:
            return render(request, 'web/sign_up.html', {})

    return render(request, 'web/COLI_main.html', {})
