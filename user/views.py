from django.shortcuts import render
from model.models import User, UserInfo, WorkTable
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
import json


# Create your views here.
def reg(request):
    if request.method == 'GET':
        return render(request, 'reg.html')
    if request.method == 'POST':
        response = HttpResponse()
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
                # 草 tm 的 username usernama，破检查器
                user = User.objects.create_user(username=username, password=password, email=email, userinfo_id=None)
            except Exception as e:
                print(e)
                resdic['status'] = -1
                resdic['msg'] = '未知错误'
                if e:
                    res.append(resdic)
                    return HttpResponse(json.dumps(res))
        else:
            try:
                user = User.objects.create_superuser(username=username, password=password, email=email, userinfo_id=None)
            except Exception as e:
                print(e)
                resdic['status'] = -1
                resdic['msg'] = '未知错误'
                if e:
                    res.append(resdic)
                    return HttpResponse(json.dumps(res))

        resdic['status'] = 1
        resdic['msg'] = '注册成功'
        resdic['uid'] = user.id
        response.set_cookie("username", username, max_age=3600*24*3)
        response.set_cookie("password", password, max_age=3600*24*3)
        res.append(resdic)
        return HttpResponse(json.dumps(res)).set_cookie('cookie', user.id, max_age=3600*24*3)


def log(request):
    if request.method == 'GET':
        return render(request, 'log.html')
    if request.method == 'POST':
        res = []
        resdic = {}
        response = HttpResponse()
        username = request.POST['username']
        password = request.POST['password']
        captcha = request.POST['captcha']
        if captcha != 'xszg':
            resdic['status'] = -3
            resdic['msg'] = '验证码错误'
            res.append(resdic)
            return HttpResponse(json.dumps(res))
        try:
            user = authenticate(username=username, password=password)
            if user:
                resdic['status'] = 1
                resdic['msg'] = '登录成功'
                resdic['uid'] = user.id
                response.set_cookie('uid', user.id, max_age=3600 * 24 * 3)
                response.set_cookie('username', username, max_age=3600*24*3)
                response.set_cookie('password', password, max_age=3600*24*3)
            else:
                resdic['status'] = 0
                resdic['msg'] = '用户名或者密码错误'
        except Exception as e:
            resdic['status'] = -1
            resdic['msg'] = '登录异常'
        res.append(resdic)

        response.write(json.dumps(res))
        return response


def add(request):
    if request.method == 'GET':
        return HttpResponseNotFound
    if request.method == "POST":
        cookie = request.COOKIES
        print(cookie)
        if not cookie:
            return HttpResponse('NO COOKIE')
        uid = cookie.get['uid']
        title = request.POST['title']
        classify = request.POST['classify']
        # goods = request.POST['goods']
        get_address = request.POST['get_address']
        home_address = request.POST['home_address']
        phone = request.POST['phone']
        # date_start = request.POST['data_start']
        # date_ending = request.POST['date_ending']
        reward = request.POST['reward']
        describe = request.POST['describe']

        print(cookie)
        return HttpResponse(200, title)


def modify(request, art_id):
    if request.method == "POST":
        req = json.loads(request.body)
        try:
            art = WorkTable.objects.get(id=art_id)
            art_id = art.id
            key_flag = req.get("title") and req.get("content") and len(req) == 2
            if key_flag:
                title = req["title"]
                content = req["content"]
                title_exist = WorkTable.objects.filter(title=title)
                if len(title_exist) > 1:
                    return JsonResponse({"status": "BS.400", "msg": "title already exist."})
                '''更新数据'''
                old_art = WorkTable.objects.get(id=art_id)
                old_art.title = title
                old_art.content = content
                old_art.save()
                return JsonResponse({"status": "BS.200", "msg": "modify article success."})
        except WorkTable.DoesNotExist:
            return JsonResponse({"status": "BS.300", "msg": "article is not exists,fail to modify."})


def delete(request, art_id):
    if request.method == "DELETE":
        try:
            art = WorkTable.objects.get(id=art_id)
            art_id = art.id
            art.delete(art_id)
            return JsonResponse({"status": "BS.200", "msg": "delete article success."})
        except WorkTable.DoesNotExist:
            return JsonResponse({"status": "BS.300", "msg": "article is not exists,fail to delete."})


def showlist(request):
    if request.method == "GET":
        articles = {}
        query_art = WorkTable.objects.all()
        for title in query_art:
            articles[title.title] = title.status
        return JsonResponse({"status": "BS.200", "all_titles": articles, "msg": "query articles success."})
