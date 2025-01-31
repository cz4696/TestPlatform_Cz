# -*- coding: utf-8 -*-
from django.urls import path, include

from . import views

app_name = 'Api'  # 声明app
urlpatterns = [
    path('get_pj_data/', views.get_pj_data, name='get_pj_data'),
    path('get_inter_data/', views.get_inter_data, name='get_inter_data'),
    path('project_data/', views.project_data, name='project_data'),
    path('perform_data/', views.perform_data, name='perform_data'),
]
