from django.shortcuts import render
from model.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json


# Create your views here.
def reg(request):
    if request.method == 'GET':
        return render(request, 'reg.html')
    if request.method == 'POST':
        res = []
        resdic = {}
        username = request.POST['username']
        password = request.POST['password']
        password_again = request.POST['password_again']
        if password != password_again:
            resdic['status'] = 0
            resdic['msg'] = '两次输入的密码不一致'
            res.append(resdic)
            return HttpResponse(json.dumps(res))

        email = request.POST['email']
        is_superuser = request.POST['is_superuser']
        if not is_superuser:
            try:
                user = User.objects.create_user(usernama=username, password=password, email=email, userinfo_id=None)
            except Exception as e:
                print(e)
                resdic['status'] = -1
                resdic['msg'] = '未知错误'
                res.append(resdic)
                return HttpResponse(json.dumps(res))
        else:
            try:
                user = User.objects.create_superuser(username=username, password=password, email=email, userinfo_id=None)
            except Exception as e:
                print(e)
                resdic['status'] = -1
                resdic['msg'] = '未知错误'
                res.append(resdic)
                return HttpResponse(json.dumps(res))
        resdic['status'] = 1
        resdic['msg'] = '注册成功'
        resdic['uid'] = user.id
        res.append(resdic)
        return HttpResponse(json.dumps(res))


def log(request):
    if request.method == 'GET':
        return render(request, 'log.html')
    if request.method == 'POST':
        res = []
        resdic = {}
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            if user:
                resdic['status'] = 1
                resdic['msg'] = '登录成功'
                resdic['uid'] = user.id
            else:
                resdic['status'] = 0
                resdic['msg'] = '用户名或者密码错误'
        except Exception as e:
            resdic['status'] = -1
            resdic['msg'] = '登录异常'

        res.append(resdic)
        return HttpResponse(json.dumps(res))


