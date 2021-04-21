import ast
from string import Template
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
from . import models
from .models import Project_Data, Interface_Data
import datetime, time
import unittest
import time
import os
from . import HTMLTestRunnerCN


# from .test_case import suite


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


def Project_Info(request):  # 项目信息跳转
    pj_name = request.POST.get('pj_name')
    if pj_name != None:
        global pjName
        pjName = pj_name
        return render(request, 'Page/Project_Info.html', {'pj_name': pjName})
    return render(request, 'Page/Project_Info.html', {'pj_name': pjName})


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


def Delete_Pj(request):  # 删除项目信息及项目下的接口信息
    if request.method == "POST":
        data_id = request.POST.get('data_id')  # 获取前端ajax传入的值
        models.Project_Data.objects.filter(id=data_id).delete()
        data_list = models.Interface_Data.objects.all().values()
        for i in data_list:  # 获得列表中的每个字典
            for key, value in i.items():  # 获取字典中的每个字段及value
                if key == 'status' and str(value) == data_id and value is not None:  # 只把status存入status_arr列表中
                    models.Interface_Data.objects.filter(status=data_id).delete()  # 当删除项目时将项目下的接口信息一同删除
                else:
                    continue
    return render(request, 'Page/Interface_List.html')


def Batch_Delete_If(request):  # 批量删除接口信息
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


def Batch_Perform_If(request):  # 批量执行功能
    if request.method == "POST":
        arr = request.POST.get('arr')
        data = json.loads(arr)
        for i in data:  # 获得列表中的每个字典
            if i['in_type'].upper() == 'POST':
                res = requests.post(url=i['in_url'], data=i['in_data'],
                                    json=json.dumps(i['in_data']))  # 接口执行方法 使用requests库处理接口
                models.Interface_Data.objects.filter(id=i['id']).update(
                    in_actual_result=res.status_code)  # res.status_code获取code对应value值
                continue
            elif i['in_type'].upper() == 'GET':
                res = requests.get(url=i['in_url'], params=i['in_data'])
                models.Interface_Data.objects.filter(id=i['id']).update(in_actual_result=res.status_code)
                continue
        return render(request, 'Page/Perform_Result.html')


def Perform_Result2(request):
    return render(request, 'Page/Perform_Result.html')


def Batch_Delete_Pj(request):  # 批量删除接口信息
    if request.method == "POST":
        arr = request.POST.get('arr')  # 获得前端JSON.stringify(data);传回的一个列表
        data = json.loads(arr)  # 将获得到的json数据转化成python类型数据（列表中包含多个字典 type(data)为列表）
        id_arr = []  # 创建一个列表存放解析出来的id
        for i in data:  # 获得列表中的每个字典
            for key, value in i.items():  # 获取字典中的每个字段及value
                if key == 'id':  # 只把id存入id_arr列表中
                    id_arr.append(value)
        for j in id_arr:  # 循环列表按照id值进行删除操作
            models.Project_Data.objects.filter(id=j).delete()
        return render(request, 'Page/Interface_List.html')
    return render(request, 'Page/Interface_List.html')


def Update_Data_If(request):  # 修改接口信息
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


def Update_Data_Pj(request):  # 修改项目信息
    if request.method == "POST":
        id = request.POST.get('data_id')
        field = request.POST.get('field')
        value = request.POST.get('value')
        if field == 'pj_id':
            models.Project_Data.objects.filter(id=id).update(pj_id=value)
        elif field == 'pj_name':
            models.Project_Data.objects.filter(id=id).update(pj_name=value)
        elif field == 'pj_pname':
            models.Project_Data.objects.filter(id=id).update(pj_pname=value)
        elif field == 'pj_tname':
            models.Project_Data.objects.filter(id=id).update(pj_tname=value)
        else:
            models.Project_Data.objects.filter(id=id).update(pj_state=value)
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


def Pj_UploadExcel(request):
    id = request.POST.get('id')
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
                                                       in_actual_result=in_actual_result,
                                                       status=id)
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


def Report(request):
    if request.method == "POST":  # 点击生成报告，全选需要生成报告的接口，将接口数据传递到这，进行处理
        arr = request.POST.get('arr')
        data = json.loads(arr)
        for i in data:
            if i['in_type'].upper() == 'POST':
                tplFilePath = r'/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/TestPlatform_User/templates/File/Template_Post.py'
                path = r'/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/TestPlatform_User/templates/File/'
                ClassNameList = []
                UrlList = []
                DataList = []
                ClassNameList.append(i['in_mname'])
                UrlList.append(i['in_url'])
                DataList.append(i['in_data'])
                for className in ClassNameList:
                    for urlName in UrlList:
                        for dataList in DataList:
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            filename = 'test_' + str(className) + '.py'  # 必须要以test为开头
                            tplFile = open(tplFilePath)
                            gFile = open(path + filename, "w")
                            lines = []
                            tpl = Template(tplFile.read())
                            lines.append(tpl.substitute(
                                now=now,
                                ClassName=className,
                                UrlName=urlName,
                                Data=dataList,
                            ))
                            gFile.writelines(lines)
                            tplFile.close()
                            gFile.close()
                            print('%s文件创建完成' % filename)
                            continue
            elif i['in_type'].upper() == 'GET':
                tplFilePath = r'/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/TestPlatform_User/templates/File/Template_Get.py'
                path = r'/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/TestPlatform_User/templates/File/'
                ClassNameList = []
                UrlList = []
                DataList = []
                ClassNameList.append(i['in_mname'])
                UrlList.append(i['in_url'])
                DataList.append(i['in_data'])
                for className in ClassNameList:
                    for params in DataList:
                        for urlName in UrlList:
                            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            filename = 'test_' + str(className) + '.py'  # 必须要以test为开头
                            tplFile = open(tplFilePath)
                            gFile = open(path + filename, "w")
                            lines = []
                            tpl = Template(tplFile.read())
                            lines.append(tpl.substitute(
                                now=now,
                                ClassName=className,
                                Params=params,
                                UrlName=urlName,
                            ))
                            gFile.writelines(lines)
                            tplFile.close()
                            gFile.close()
                            print('%s文件创建完成' % filename)
                            continue
    test_dir = '/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/TestPlatform_User/templates/File'
    filepath = '/Users/caozheng/Library/Preferences/PyCharm2018.3/TestPlatform_Cz/InterfaceTestPlatform/report/TestReport.html'

    def allcase():
        discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")
        # discover方法筛选出来的用例，循环添加到测试套件中
        suite = unittest.TestSuite()
        suite.addTest(discover)
        print(discover)
        return suite

    fp = open(filepath, 'wb')
    # 定义测试报告的标题与描述
    runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=u'测试报告', description=u'测试报告描述')
    runner.run(allcase())
    fp.close()
    return render(request, 'Page/Perform_Result.html')
