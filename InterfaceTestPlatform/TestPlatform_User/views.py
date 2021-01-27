from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout  # 从app导入
from django.contrib.auth.forms import UserCreationForm  # 自带创建用户表单，注册


# Create your views here.

def Home(request):  # 首页
    return render(request, 'Page/home.html')


def Login(request):  # 登录功能
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            # username = {'name': request.user.username}
            return render(request, 'Page/login.html', {'error': '用户名或密码不正确'})
        else:
            login(request, user)  # 登录函数
            # username = request.user.username
            # name = request.session['username'] = username
            # return render(request,'',name)
            request.user.get_username()
            return redirect('TestPlatform_User:Home')  # 重定向
    else:
        return render(request, 'Page/login.html')


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
            return redirect('TestPlatform_User:Page')
    else:
        register_form = UserCreationForm()
    content = {"register_form": register_form}
    return render(request, 'Page/register.html', content)
