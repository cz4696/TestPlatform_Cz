import ast
from venv import logger

import yagmail
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout  # 从app导入
from django.contrib.auth.forms import UserCreationForm  # 自带创建用户表单，注册
import xlrd, xlwt, json, sys
import requests
from idna import unicode
from . import Import_Excel, models
from .models import Project_Data, Interface_Data
from pygments import highlight, lexers, formatters
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


def Project_Info(request):  # 项目列表跳转
    return render(request, 'Page/Project_Info.html')


def Interface_List(request):  # 接口列表跳转
    return render(request, 'Page/Interface_List.html')


def Interface_Perform(request):  # 单条接口执行
    if request.method == "POST":
        in_url = request.POST.get('in_url')
        in_data = request.POST.get('in_data')
        in_expected_result = request.POST.get('in_expected_result')
        in_type = request.POST.get('in_type')
        if in_type == 'POST':
            res = requests.post(url=in_url, data=in_data, json=json.dumps(in_data))
            result = res.json()
            in_data_json = json.dumps(result, indent=4, ensure_ascii=False, sort_keys=True)
            # colorfule_json = highlight(in_data_json,lexers.JsonLexer(),formatters.TerminalFormatter())    # json美化
            in_actual_result = res.status_code  # 获取code对应value值
            if int(in_actual_result) == int(in_expected_result):  # 需要转换为int，虽然看着一样，但类型不同，string类型
                return render(request, 'Page/Interface_Perform.html',
                              {'json_msg': in_data_json, 'headers_msg': res.headers, 'actual_result': in_actual_result,
                               'state': '测试通过！'})
            else:
                return render(request, 'Page/Interface_Perform.html',
                              {'state': '测试不通过,预期结果与实际结果不符！', 'actual_result': in_actual_result})
        elif in_type == 'GET':
            res = requests.get(url=in_url, params=in_data)
            # in_data_json = json.dumps(res, indent=4, ensure_ascii=False, sort_keys=True)
            in_actual_result = res.status_code
            if int(in_actual_result) == int(in_expected_result):
                return render(request, 'Page/Interface_Perform.html',
                              {'json_msg': res, 'headers_msg': res.headers,
                               'actual_result': in_actual_result,
                               'state': '测试通过！'})
            else:
                return render(request, 'Page/Interface_Perform.html',
                              {'json_msg': 'ERROR!预期结果与实际结果不符！' + str(in_actual_result),
                               'state': '测试不通过,预期结果与实际结果不符！',
                               'actual_result': in_actual_result})

        return render(request, 'Page/Interface_Perform.html')
    else:
        return render(request, 'Page/Interface_Perform.html')


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


def Delete_Data(request):  # 删除接口信息
    if request.method == "POST":
        data_id = request.POST.get('data_id')  # 获取前端ajax传入的值
        models.Interface_Data.objects.filter(id=data_id).delete()
    return render(request, 'Page/Interface_List.html')


def Batch_Delete(request):  # 批量删除接口信息
    if request.method == "POST":
        arr = request.POST.get('arr')  # 获得前端JSON.stringify(data);传回的一个列表
        data = json.loads(arr)  # 将获得到的json数据转化成python类型数据（列表中包含多个字典 type(data)为列表）
        id_arr = []  # 创建一个列表存放解析出来的id
        for i in data:  # 获得列表中的每个字典
            for key, value in i.items():  # 获取字典中的每个字段及value
                if key == 'id':  # 只把id存入id_arr列表中
                    id_arr.append(value)
        for j in id_arr:  # 循环列表按照id值进行删除操作
            models.Interface_Data.objects.filter(id=j).delete()
        return render(request, 'Page/Interface_List.html')
    return render(request, 'Page/Interface_List.html')


def Update_Data(request):  # 修改接口信息
    if request.method == "POST":
        id = request.POST.get('data_id')
        field = request.POST.get('field')
        value = request.POST.get('value')
        if field == 'in_id':
            models.Interface_Data.objects.filter(id=id).update(in_id=value)
        elif field == 'in_mname':
            models.Interface_Data.objects.filter(id=id).update(in_mname=value)
        elif field == 'in_type':
            models.Interface_Data.objects.filter(id=id).update(in_type=value)
        elif field == 'in_url':
            models.Interface_Data.objects.filter(id=id).update(in_url=value)
        elif field == 'in_data':
            models.Interface_Data.objects.filter(id=id).update(in_data=value)
        elif field == 'in_data_type':
            models.Interface_Data.objects.filter(id=id).update(in_data_type=value)
        elif field == 'in_tname':
            models.Interface_Data.objects.filter(id=id).update(in_tname=value)
        else:
            models.Interface_Data.objects.filter(id=id).update(in_expected_result=value)
    return render(request, 'Page/Interface_List.html')


def Select_Data(request):
    if request.method == 'POST':
        in_id = request.POST.get('searchData')
        print(in_id)
        models.Interface_Data.objects.filter(in_id=in_id)   # QuerySet结果集，不能直接使用json.dumps序列化
        # json_list = []
        # for i in get_data:
        #     json_dict = {}
        #     json_dict['in_id'] = i.in_id
        #     json_list.append(json_dict)
        # print(json_list)
        # return JsonResponse(json_list,safe=False)
    return render(request, 'Page/Interface_List.html')


def UploadExcel(request):
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
                        in_data_type = data_list[i - 1][4]
                        in_data = data_list[i - 1][5]
                        in_tname = data_list[i - 1][6]
                        in_expected_result = data_list[i - 1][7]
                        in_actual_result = data_list[i - 1][8]
                        add_interface = Interface_Data(in_id=in_id, in_mname=in_mname, in_type=in_type,
                                                       in_url=in_url,
                                                       in_data_type=in_data_type, in_data=in_data,
                                                       in_tname=in_tname,
                                                       in_expected_result=in_expected_result,
                                                       in_actual_result=in_actual_result)
                        add_interface.save()

            except:
                logger.error('解析excel文件或者数据插入错误')
            return HttpResponse(json.dumps(data_list), {'message': '导入成功'})
            # return render(request, 'Page/Interface_List.html', {'message': '导入成功'})
        else:
            logger.error('上传文件类型错误！')
            return render(request, 'Page/Interface_List.html', {'message': '导入失败'})


# 邮件发送方法
def SendMail(title, msg, receivers):
    yag = yagmail.SMTP(
        host='smtp.qq.com', user='469687182@qq.com',
        password='ppbdsowziqnlbhha', smtp_ssl=True
    )

    try:
        yag.send(receivers, title, msg)
        print("邮件发送成功！")

    except BaseException as e:
        print(e)
        print("Error: 发送邮件失败！")


def Edit_Project(request):
    return render(request, 'Page/Edit_Project.html')


def Detail_Project(request):
    return render(request, 'Page/Detail_Project.html')
