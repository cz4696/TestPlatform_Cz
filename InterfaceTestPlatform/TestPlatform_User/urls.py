# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'TestPlatform_User' # 声明app
urlpatterns = [
    path('home/', views.Home, name='Home'),
    path('', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),
]
