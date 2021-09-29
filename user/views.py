from django.shortcuts import render
from model.models import User, UserInfo, WorkTable, TableDeal
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
import json
from django.db.models import Q
import datetime


def datetime_str_parse(str_datetime):
    strlist = str_datetime.split(' ')
    date_list = strlist[0].split('-')
    time_list = strlist[1].split(':')
    return datetime.datetime(int(date_list[0]),int(date_list[1]), int(date_list[2]), int(time_list[0]), int(time_list[1]), int(time_list[2]))


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
        uid = request.COOKIES['uid']
        if uid:
            user = User.objects.get(id=uid)
            if user.is_superuser:
                return HttpResponseRedirect('/admin_site/')
            else:
                return render(request, 'pages/login.html')
        else:
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
    if classify == 'take':
        classify = '帮我取'
    elif classify == 'do':
        classify = '帮我做'
    elif classify == 'buy':
        classify = '帮我买'
    else:
        classify = '?'
    goods = request.POST['goods']
    get_address = request.POST['get_address']
    home_address = request.POST['home_address']
    phone = request.POST['phone']
    date_start = datetime_str_parse(request.POST['date_start'])
    date_ending = datetime_str_parse(request.POST['date_ending'])
    reward = request.POST['reward']
    describe = request.POST['describe']
    try:
        tableinfo = WorkTable.objects.create(title=title, classify=classify, goods=goods, get_address=get_address,
                                         home_address=home_address, phone=phone, date_start=date_start, date_ending=date_ending,
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
        res_dict = {
            'code': 0,
            'msg': '成功',
            'count': 1,
        }
        res = {}
        if userinfo:
            res['username'] = user.username
            res['name'] = userinfo.name
            res['sex'] = userinfo.sex
            res['stu_num'] = userinfo.student_num
            res['email'] = user.email
            res['money'] = userinfo.money
            res_dict['data'] = [res, ]
            response.write(json.dumps(res_dict))
        elif not userinfo:
            res['username'] = user.username
            res['name'] = 'xxx'
            res['sex'] = '男'
            res['stu_num'] = 0
            res['email'] = user.email
            res['money'] = 0
            res_dict['data'] = [res, ]
            response.write(json.dumps(res_dict))
        return response
    if request.method == 'POST':
        uid = request.COOKIES['uid']
        post_dict = request.POST
        username = post_dict['username']
        sex = post_dict['sex']
        email = post_dict['email']
        user = User.objects.get(id=uid)
        userinfo_id = user.userinfo_id
        if userinfo_id:
            userinfo = UserInfo.objects.get(id=user.userinfo_id)
            userinfo.sex = sex
            userinfo.save()
        elif not userinfo_id:
            pass
        user.username = username
        user.email = email
        user.save()
        res = {
            'code': 1,
            'msg': '成功',
        }
        return HttpResponse(json.dumps(res))


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
        tables = TableDeal.objects.filter(User_request_id=user.id, isActive=1)
        for table in tables:
            table_dict = {}
            state = 0
            if table.isActive == 1:
                table_info = WorkTable.objects.get(id=table.Table_id)
                username_runner = '无'
                username_runner_id = table.User_receive_id
                if username_runner_id:
                    username_runner = User.objects.get(id=username_runner_id).username
                if table_info.isFinished:
                    state = 1
                if state:
                    state_str = '已完成'
                else:
                    state_str = '未完成'
                table_dict['table_id'] = table.id
                table_dict['title'] = table_info.title
                table_dict['classify'] = table_info.classify
                table_dict['goods'] = table_info.goods
                table_dict['get_address'] = table_info.get_address
                table_dict['home_address'] = table_info.home_address
                table_dict['phone'] = table_info.phone
                table_dict['state'] = state_str
                table_dict['runner'] = username_runner
                table_dict['date_start'] = table_info.date_start+datetime.timedelta(hours=8)
                table_dict['date_ending'] = table_info.date_ending+datetime.timedelta(hours=8)
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
        res = {}
        post_dict = request.POST
        cookie = request.COOKIES
        password_old = post_dict['password_old']
        password_new = post_dict['password_new']
        # print(password_new)
        user = User.objects.get(id=cookie['uid'])
        ok = user.check_password(raw_password=password_old)
        if ok:
            user.set_password(password_new)
            user.save()
            res['state'] = 1
        else:
            res['state'] = 0
        return HttpResponse(json.dumps(res))


@check_login
def help(request):
    if request.method == 'GET':
        return render(request, 'pages/user-help.html')
    if request.method == 'POST':
        uid = request.COOKIES['uid']
        user = User.objects.get(id=uid)
        response = HttpResponse()
        res = {
            'code': 0,
            'msg': '成功',
        }
        item_list = []
        tables = TableDeal.objects.filter(isActive=1)
        for table in tables:
            state = 0
            if str(table.User_receive_id) == uid:
                tableinfo = WorkTable.objects.get(id=table.Table_id)
                if tableinfo.isFinished:
                    state = 1
                if state:
                    state_str = '已完成'
                else:
                    state_str = '未完成'
                _dict = {
                    'table_id': table.id,
                    'title': tableinfo.title,
                    'goods': tableinfo.goods,
                    'classify': tableinfo.classify,
                    'phone': tableinfo.phone,
                    'username': user.username,
                    'reward': tableinfo.back,
                    'state': state_str,
                    'get_address': tableinfo.get_address,
                    'home_address': tableinfo.home_address,
                    'date_start': tableinfo.date_start,
                    'date_end': tableinfo.date_ending,
                    'describe': tableinfo.describe,
                }
                item_list.append(_dict)
        res['data'] = item_list
        response.write(json.dumps(res, cls=DateEncoder))
        return response


@check_login
def order(request):
    if request.method == 'GET':
        return render(request, 'pages/order.html')
    if request.method == 'POST':
        uid = request.COOKIES['uid']
        table_deal_id = request.POST['table_id']
        table_info = TableDeal.objects.get(id=int(table_deal_id))
        table_id = table_info.Table_id
        table = WorkTable.objects.get(id=table_id)
        table_info.User_receive_id = uid
        table_info.save()
        table.isAccept = 1
        table.save()
        res = {
            'code': 0,
            'msg': '接单成功',
        }
        return HttpResponse(json.dumps(res))


@check_login
def order_list(request):
    if request.method == 'GET':
        res = {
            'code': 0,
        }
        response = HttpResponse()
        table_deal_all = TableDeal.objects.filter(isActive=1)
        item_list = []
        for item in table_deal_all:
            if not item.User_receive_id:
                user = User.objects.get(id=item.User_request_id)
                tableinfo = WorkTable.objects.get(id=item.Table_id)
                _dict = {
                    'id': item.id,
                    'title': tableinfo.title,
                    'goods': tableinfo.goods,
                    'classify': tableinfo.classify,
                    'phone': tableinfo.phone,
                    'username': user.username,
                    'reward': tableinfo.back,
                    'get_address': tableinfo.get_address,
                    'home_address': tableinfo.home_address,
                    'date_start': tableinfo.date_start+datetime.timedelta(hours=8),
                    'date_end': tableinfo.date_ending+datetime.timedelta(hours=8),
                    'describe': tableinfo.describe,
                }
                item_list.append(_dict)
        res['data'] = item_list
        response.write(json.dumps(res, cls=DateEncoder))
        return response


@check_login
def get_list(request):
    if request.method == 'GET':
        res = {
            'code': 0,
        }
        response = HttpResponse()
        table_deal_all = TableDeal.objects.all()
        item_list = []
        for item in table_deal_all:
            if not item.User_receive_id:
                state = 0
                user = User.objects.get(id=item.User_request_id)
                tableinfo = WorkTable.objects.get(id=item.Table_id)
                if tableinfo.isFinished:
                    state = 1
                if state:
                    state_str = '已完成'
                else:
                    state_str = '未完成'
                _dict = {
                    'id': item.Table_id,
                    'title': tableinfo.title,
                    'goods': tableinfo.goods,
                    'classify': tableinfo.classify,
                    'phone': tableinfo.phone,
                    'username': user.username,
                    'reward': tableinfo.back,
                    'state': state_str,
                    'get_address': tableinfo.get_address,
                    'home_address': tableinfo.home_address,
                    'date_start': tableinfo.date_start+datetime.timedelta(hours=8),
                    'date_end': tableinfo.date_ending+datetime.timedelta(hours=8),
                    'describe': tableinfo.describe,
                }
                item_list.append(_dict)
        res['data'] = item_list
        response.write(json.dumps(res, cls=DateEncoder))
        return response


@check_login
def del_table(request):
    if request.method == 'POST':
        table_id = int(request.POST['table_id'])
        print(table_id)
        table_deal = TableDeal.objects.get(id=table_id)
        table = WorkTable.objects.get(id=table_deal.Table_id)
        table_deal.isActive = 0
        table.isActive = 0
        table_deal.save()
        table.save()
        res = {
            'code': 0,
            'msg': '删除成功',
        }
        return HttpResponse(json.dumps(res))


@check_login
def finish_table(request):
    if request.method == 'POST':
        table_deal_id = request.POST['table_id']
        table_id = TableDeal.objects.get(id=table_deal_id).Table_id
        table = WorkTable.objects.get(id=table_id)
        table.isFinished = True
        table.save()
        res = {
            'code': 0,
            'msg': '成功',
        }
        return HttpResponse(json.dumps(res))


def update(request):
    if request.method == 'POST':
        table_post = request.POST
        table_deal_id = request.POST['table_id']
        # 草 直接暴力更改吧
        table_deal = TableDeal.objects.get(id=table_deal_id)
        table_info = WorkTable.objects.get(id=table_deal.Table_id)
        table_info.title = table_post['information[title]']
        table_info.classify = table_post['information[classify]']
        table_info.goods = table_post['information[goods]']
        table_info.get_address = table_post['information[get-address]']
        table_info.home_address = table_post['information[home_address]']
        table_info.phone = table_post['information[phone]']
        table_info.date_start = table_post['information[date_start]']
        table_info.date_ending = table_post['information[date_ending]']
        table_info.back = table_post['information[reward]']
        table_info.describe = table_post['information[describe]']
        table_info.save()
        print(table_info)
        res = {
            'code': 0,
            'msg': '更改成功'
        }
        return HttpResponse(json.dumps(res))




