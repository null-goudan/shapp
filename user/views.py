from django.shortcuts import render
from model.models import User, UserInfo, WorkTable, TableDeal
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
import json
import datetime


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.POST or 'uid' not in request.POST:
            cookie_username = request.COOKIES.get('username')
            cookie_uid = request.COOKIES.get('uid')
            if not cookie_username or not cookie_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = cookie_username
                request.session['uid'] = cookie_uid
        return fn(request, *args, **kwargs)
    return wrap


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


# Create your views here.
def reg(request):
    if request.method == 'GET':
        return render(request, 'pages/logon.html')
    if request.method == 'POST':
        if request.POST['step'] == '1':
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
            user_type = request.POST['user']
            if user_type == 'users':
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
            elif user_type == 'is_superuser':
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
            response.set_cookie("uid", user.id, max_age=3600*24*3)
            res.append(resdic)
            response.write(json.dumps(res))
            return response
        elif request.POST['step'] == '2':
            response = HttpResponse()
            res = []
            resdic = {}
            cookie_user = request.COOKIES
            print(cookie_user)
            sex = request.POST['sex']
            age = request.POST['age']
            student_name = request.POST['name']
            student_num = request.POST['schoolnumber']
            # TODO 写一个认证
            #
            userinfo = object
            try:
                userinfo = UserInfo.objects.create(name=student_name, sex=sex, age=age, student_num=student_num, score=0, money=0)
            except Exception as e:
                print("exception---"+e)
                resdic['status'] = -1
                resdic['msg'] = '认证失败,服务器原因'
            try:
                user = User.objects.get(id=cookie_user['uid'])
                user.userinfo = userinfo
                user.save()
                resdic['status'] = 1
                resdic['msg'] = '认证成功'
            except Exception as e:
                print("exception---" + e)
                resdic['status'] = -1
                resdic['msg'] = '认证失败,服务器原因'
            res.append(resdic)
            response.write(json.dumps(res))
            return response


def houtai_log(request):
    if request.method == 'GET':
        return render(request, 'pages/login.html')
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
            if user.is_superuser:
                resdic['status'] = 1
                resdic['msg'] = '登录成功'
                resdic['uid'] = user.id
                response.set_cookie('uid', user.id, max_age=3600 * 24 * 3)
                response.set_cookie('username', username, max_age=3600*24*3)
                response.set_cookie('password', password, max_age=3600*24*3)
            elif not user.is_superuser:
                resdic['status'] = -1
                resdic['msg'] = '不是管理员'
            else:
                resdic['status'] = 0
                resdic['msg'] = '用户名或者密码错误'
        except Exception as e:
            resdic['status'] = -1
            resdic['msg'] = '登录异常'
        res.append(resdic)

        response.write(json.dumps(res))
        return response


def log(request):
    if request.method == 'GET':
        return render(request, 'pages/login-index.html')
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


def __post_and_add(request):
    res_list=[]
    res_dict={}
    cookie = request.COOKIES
    if not cookie:
        return HttpResponse('NO COOKIE')
    uid = cookie.get('uid')
    title = request.POST['title']
    classify = request.POST['classify']
    goods = request.POST['goods']
    get_address = request.POST['get_address']
    home_address = request.POST['home_address']
    phone = request.POST['phone']
    date_start = request.POST['date_start']
    date_ending = request.POST['date_ending']
    reward = request.POST['reward']
    describe = request.POST['describe']
    try:
        tableinfo = WorkTable.objects.create(title=title, classify=classify,goods=goods,get_address=get_address,
                                         home_address=home_address, phone=phone,date_start=date_start, date_ending=date_ending,
                                         back=reward, BackType=1, describe=describe)
    except Exception as e:
        print(e)
        res_dict['status'] = -1
        res_dict['msg'] = '添加单子失败,服务器问题'
        res_list.append(res_dict)
        return json.dumps(res_list)

    try:
        tabledeal = TableDeal.objects.create(Table_id=tableinfo.id, User_request_id=uid, isActive=True)
    except Exception as e:
        print(e)
        res_dict['status'] = -1
        res_dict['msg'] = '添加单子失败,服务器问题'
        res_list.append(res_dict)
        return json.dumps(res_list)
    res_dict['status'] = 1
    res_dict['msg'] = '添加单子成功'
    res_list.append(res_dict)
    return json.dumps(res_list)


@check_login
def add_take(request):
    if request.method == 'GET':
        return render(request, 'pages/take.html')

    if request.method == "POST":
        response = HttpResponse()
        res_dict = __post_and_add(request)
        response.write(res_dict)
        return response


@check_login
def add_do(request):
    if request.method == 'GET':
        return render(request, 'pages/do.html')
    if request.method == "POST":
        response = HttpResponse()
        res_dict = __post_and_add(request)
        response.write(res_dict)
        return response


@check_login
def add_buy(request):
    if request.method == 'GET':
        return render(request, 'pages/buy.html')
    if request.method == "POST":
        response = HttpResponse()
        res_dict = __post_and_add(request)
        response.write(res_dict)
        return response


@check_login
def infomation(request):
    if request.method == 'GET':
        return render(request, 'pages/user-information.html')


@check_login
def information_userinfo(request):
    if request.method == 'GET':
        response = HttpResponse()
        cookie = request.COOKIES
        if not cookie:
            return HttpResponseNotFound()
        user = User.objects.get(id=cookie.get('uid'))
        userinfo = user.userinfo
        res = {}
        if userinfo:
            res['username'] = user.username
            res['name'] = userinfo.name
            res['sex'] = userinfo.sex
            res['stu_num'] = userinfo.student_num
            res['email'] = user.email
            res['money'] = userinfo.money
            response.write(json.dumps(res))
        elif not userinfo:
            res['username'] = user.username
            res['name'] = 'xxx'
            res['sex'] = '男'
            res['stu_num'] = '%%%%%%%%%'
            res['email'] = user.email
            res['money'] = '%'
            response.write(json.dumps(res))
        return response


@check_login
def send(request):
    if request.method == 'GET':
        return render(request, 'pages/user-send.html')


@check_login
def send_table_info(request):
    if request.method == 'GET':
        cookie = request.COOKIES
        if not cookie:
            return HttpResponseRedirect('/')
        table_list = []
        user = User.objects.get(id=cookie['uid'])
        tables = TableDeal.objects.filter(User_request_id=user.id)
        for table in tables:
            table_dict = {}
            if table.isActive == 1:
                table_info = WorkTable.objects.get(id=table.Table_id)
                table_dict['title'] = table_info.title
                table_dict['classify'] = table_info.classify
                table_dict['goods'] = table_info.goods
                table_dict['get_address'] = table_info.get_address
                table_dict['home_address'] = table_info.home_address
                table_dict['phone'] = table_info.phone
                table_dict['date_start'] = table_info.date_start
                table_dict['date_ending'] = table_info.date_ending
                table_dict['reward'] = table_info.back
                table_dict['describe'] = table_info.describe
                table_list.append(table_dict)
        response = {}
        response['code'] = 0
        response['msg'] = '成功'
        response['count'] = len(table_list)
        response['data'] = table_list
        return HttpResponse(json.dumps(response, cls=DateEncoder))


@check_login
def password(request):
    if request.method == 'GET':
        return render(request, 'pages/user-password.html')
    if request.method == 'POST':
        post_dict = request.POST


@check_login
def help(request):
    if request.method == 'GET':
        return render(request, 'pages/user-help.html')


@check_login
def order(request):
    if request.method == 'GET':
        return render(request, 'pages/order.html')

@check_login
def get_list(request):
    if request.method == 'GET':
        table_deal_all = TableDeal.objects.all()
        table_info_list = []
        for item in table_deal_all:
            item_dict = {}
            item_dict['tid'] = item.Table_id
            item_dict['user_request_id'] = item.User_request_id
            table_info_list.append(item_dict)
        return HttpResponse(request, json.dumps(table_info_list))

