# coli/members/web_urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page),
    path('main2/', main_page2),
    path('main3/', main_page3),
]
