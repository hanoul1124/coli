# coli/members/web_urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page),
    path('main/', main_page),
    path('main2/', main_page2),
    path('main3/', main_page3),
    path('sign_in/', sign_in_page),
    path('sign_up/', sign_up_page),
    path('login/', login),
    path('sign_up_do/', sign_up),
]
