# -*- coding: utf-8 -*-
from django.urls import path, include

from Api import views

urlpatterns = [
    path('get_pj_date/', views.get_pj_date, name='get_pj_date'),
]
