# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'TestPlatform_User'  # 声明app
urlpatterns = [
    path('home/', views.Home, name='Home'),
    path('', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),
    path('project_list/', views.Project_List, name='Project_List'),
    path('project_info/', views.Project_Info, name='Project_Info'),
    path('interface_list/', views.Interface_List, name='Interface_List'),
    path('interface_perform/', views.Interface_Perform, name='Interface_Perform'),
    path('add_project/', views.Add_Project, name='Add_Project'),
    path('add_pj/', views.Add_Pj, name='Add_Pj'),
    path('upload_excel/', views.UploadExcel, name='UploadExcel'),
    path('edit_project/', views.Edit_Project, name='Edit_Project'),
    path('detail_project/', views.Detail_Project, name='Detail_Project'),
    path('delete_data/', views.Delete_Data, name='Delete_Data'),
    path('update_data/', views.Update_Data, name='Update_Data'),
    path('batch_delete/', views.Batch_Delete, name='Batch_Delete'),
    path('select_data/', views.Select_Data, name='Select_Data'),


    # path('interface_list/', views.Interface_List, name='Interface_List'),
]
