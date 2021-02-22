from venv import logger

from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout  # 从app导入
from django.contrib.auth.forms import UserCreationForm  # 自带创建用户表单，注册
import xlrd, xlwt, json, sys
import requests
from . import Import_Excel, models
from .models import Project_Data, Interface_Data
import datetime, time


# Create your views here.
def Home(request):  # 首页
    return render(request, 'Page/Home.html')


def Login(request):  # 登录功能
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            # username = {'name': request.user.username}
            return render(request, 'Page/Login.html', {'error': '用户名或密码不正确'})
        else:
            login(request, user)  # 登录函数
            request.user.get_username()  # request传递登录的用户名
            return redirect('TestPlatform_User:Home')  # 重定向到Home 详情见url中
    else:
        return render(request, 'Page/Login.html')


def Logout(request):  # 登出功能
    logout(request)
    return redirect('TestPlatform_User:Login')  # 重定向


def Register(request):  # 注册功能
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():  # 返回真假，表单是否填写正确
            register_form.save()  # 保存到后台
            user = authenticate(username=register_form.cleaned_data['username'],
                                password=register_form.cleaned_data['password1'])
            login(request, user)
            return redirect('TestPlatform_User:Home')
    else:
        register_form = UserCreationForm()
    content = {"register_form": register_form}
    return render(request, 'Page/Register.html', content)


def Project_List(request):  # 项目列表跳转
    return render(request, 'Page/Project_List.html')


def Interface_List(request):  # 接口列表跳转
    return render(request, 'Page/Interface_List.html')


def Interface_Perform(request):  # 一个接口执行
    pt = Import_Excel.cls_api()
    exr = request.POST.get('exr', None)
    data = ""
    data1 = ""
    if request.method == 'POST':
        data = pt.post(request.POST.get('url', None), json.loads(request.POST.get('testdate', None)))
        result = data.json()
        data1 = result['message']
        if int(result['message'] == int(exr)):
            data = u'测试通过'
        else:
            data = u'测试失败'
    return render(request, 'Page/Interface_Perform.html', {"data": data, "data1": data1})


def add_args(a, b):
    x = int(a)
    y = int(b)
    return x + y


def post(request):
    if request.method == 'POST':
        d = {}
        if request.POST:
            a = request.POST.get('a', None)
            b = request.POST.get('b', None)
            if a and b:
                res = add_args(a, b)
                d['message'] = res
                d = json.dumps(d)
                return HttpResponse(d)
            else:
                return HttpResponse(u'输入错误')
        else:
            return HttpResponse(u'输入为空')
    else:
        return HttpResponse(u'方法错误')


def Add_Project(request):  # 点击新增跳转出页面
    return render(request, 'Page/Add_Project.html')


def Add_Pj(request):  # 添加部门信息
    if request.method == 'POST':
        pj_id = request.POST.get('pj_id')
        pj_name = request.POST.get('pj_name')
        pj_pname = request.POST.get('pj_pname')
        pj_tname = request.POST.get('pj_tname')
        pj_state = request.POST.get('pj_state')
        add_project = Project_Data(pj_id=pj_id, pj_name=pj_name, pj_pname=pj_pname, pj_tname=pj_tname,
                                   pj_state=pj_state)
        add_project.save()
        return HttpResponse()


def uploadtest(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            data_list = []  # 获取表中数据
            try:
                for i in range(rows):
                    if i != 0:
                        data_list.append(table.row_values(i))
                        in_id = data_list[i - 1][0]
                        in_mname = data_list[i - 1][1]
                        in_type = data_list[i - 1][2]
                        in_url = data_list[i - 1][3]
                        in_data = data_list[i - 1][4]
                        in_tname = data_list[i - 1][5]
                        in_expected_result = data_list[i - 1][6]
                        in_actual_result = data_list[i - 1][7]
                        add_interface = Interface_Data(in_id=in_id, in_mname=in_mname, in_type=in_type, in_url=in_url,
                                                       in_data=in_data, in_tname=in_tname,
                                                       in_expected_result=in_expected_result,
                                                       in_actual_result=in_actual_result)
                        add_interface.save()
                        # return HttpResponse()
            except:
                logger.error('解析excel文件或者数据插入错误')
            return render(request, 'Page/Interface_List.html', {'message': '导入成功'})
        else:
            logger.error('上传文件类型错误！')
            return render(request, 'Page/Interface_List.html', {'message': '导入失败'})
