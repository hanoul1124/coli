# coli/members/urls.py
from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('keygen/', views.generate_user_key, name='keygen'),
    path('pidgen/', views.create_pid, name='pidgen'),
    path('owners/', views.owners_view, name='owners'),
]
