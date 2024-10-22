# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views
from django.contrib import admin

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
    path('sendemail/', views.SendMail, name='SendMail'),
    path('SendEmail/', views.SendEmail, name='SendEmail'),
    path('upload_excel/', views.UploadExcel, name='UploadExcel'),
    path('edit_project/', views.Edit_Project, name='Edit_Project'),
    path('detail_project/', views.Detail_Project, name='Detail_Project'),
    path('delete_data/', views.Delete_Data, name='Delete_Data'),
    path('delete_pj/', views.Delete_Pj, name='Delete_Pj'),
    path('update_data_if/', views.Update_Data_If, name='Update_Data_If'),
    path('batch_delete_if/', views.Batch_Delete_If, name='Batch_Delete_If'),
    path('batch_delete_pj/', views.Batch_Delete_Pj, name='Batch_Delete_Pj'),
    path('update_data_pj/', views.Update_Data_Pj, name='Update_Data_Pj'),
    path('pj_uploadexcel/', views.Pj_UploadExcel, name='Pj_UploadExcel'),
    path('batch_perform_if/', views.Batch_Perform_If, name='Batch_Perform_If'),
    path('perform_result/', views.Perform_Result, name='Perform_Result'),
    path('report/', views.Report, name='Report'),

]
