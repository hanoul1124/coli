from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import User
import datetime

# Create your views here.
def main_page(request):
    return render(request, 'web/COLI_main.html', {'signup': False})

def main_page2(request):
    return render(request, 'web/main2.html', {})

def main_page3(request):
    return render(request, 'web/main3.html', {})

def sign_in_page(request):
    return render(request, 'web/sign_in.html', {'error': False})

def sign_up_page(request):
    return render(request, 'web/sign_up.html', {'signup_fail': False})

# Function of login process
def login(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pwd1']
        try:
            # find ID
            user = User.objects.get(username=id)
        except ObjectDoesNotExist:
            # ID does not exist.
            return render(request, 'web/sign_in.html', {'error': True})

        if not user.check_password(pw):
            # Password does not match.
            return render(request, 'web/sign_in.html', {'error': True})

        if user.authority == 'Comp':
            # Company-only web page
            return render(request, 'web/main_company.html',
            {'full_name': user.full_name, 'authority': user.get_authority_display()})
        else:
            # Default logined main page
            return render(request, 'web/main_login.html',
            {'full_name': user.full_name, 'authority': user.get_authority_display()})
    else:
        raise Http404("404 Not Found.")

# Function of sign up process
def sign_up(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pwd']
        sex = request.POST['sex']
        fullname = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        birth_year = int(request.POST['birth_year'])
        birth_month = int(request.POST['birth_month'])
        birth_day = int(request.POST['birth_day'])
        authority = request.POST['Authority']

        try:
            # User creation
            obj = User.objects.create(
                username=id, sex=sex, full_name=fullname,
                email=email, phone_number=phone,
                birthday=datetime.date(birth_year, birth_month, birth_day),
                authority=authority
            )
            obj.set_password(pw)
            obj.save()
        except ValueError:
            # ValueError exception: datetime.date error
            return render(request, 'web/sign_up.html', {'signup_fail': True})
        except ValidationError:
            # ValidationError exception: phone number validation error
            return render(request, 'web/sign_up.html', {'signup_fail': True})
    else:
        raise Http404("404 Not Found.")

    return render(request, 'web/COLI_main.html', {'signup': True})
