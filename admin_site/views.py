from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from model.models import User, TableDeal, UserInfo, WorkTable
import json
import datetime
from datetime import date


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def check_admin_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.POST or 'uid' not in request.POST:
            cookie_username = request.COOKIES.get('username')
            cookie_uid = request.COOKIES.get('uid')
            if not cookie_uid:
                return HttpResponseRedirect('/user/houtai_login')
            user = User.objects.get(id=cookie_uid)
            if not cookie_username or not cookie_uid:
                return HttpResponseRedirect('/user/houtai_login')
            if user.is_superuser == 0:
                return HttpResponseRedirect('/user/houtai_login')
            else:
                request.session['username'] = cookie_username
                request.session['uid'] = cookie_uid
        return fn(request, *args, **kwargs)
    return wrap


# Create your views here.
@check_admin_login
def index(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')


@check_admin_login
def welcome(request):
    if request.method == 'GET':
        return render(request, 'admin/page/welcome.html')
    if request.method == 'POST':
        if request.POST['msg'] == 'get_info':
            response = HttpResponse()
            res = {}
            user_count = User.objects.filter(is_active=1).count()
            table_count = TableDeal.objects.count()
            table_waiting_count = 0
            table_doing_count = 0
            table_finish_count = 0
            table_list = TableDeal.objects.filter(isActive=1)
            for item in table_list:
                if not item.User_receive_id:
                    table_waiting_count += 1
                else:
                    table_id = item.Table_id
                    tableinfo = WorkTable.objects.get(id=table_id)
                    if tableinfo.isFinished:
                        table_finish_count += 1
                    else:
                        table_doing_count += 1

            res['user_count'] = user_count
            res['table_doing_count'] = table_doing_count
            res['table_waiting_count'] = table_waiting_count
            res['table_finish_count'] = table_finish_count
            response.write(json.dumps(res))
            return response


@check_admin_login
def table_user(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_user.html')
    if request.method == 'POST':
        response = HttpResponse()
        reslist = []
        Userlist = User.objects.filter(is_active=1);
        for item in Userlist:
            print(item.userinfo_id)
            if not item.userinfo_id:
                _dict = {
                    'user_id': item.id,
                    'username': item.username,
                    'sex': "",
                    'name': '',
                    'email': item.email,
                    'schoolnumber': '',
                    'pass': 0,
                    'wealth': 0,
                }
            else:
                userinfo = UserInfo.objects.get(id=item.userinfo_id)
                _dict = {
                    'user_id': item.id,
                    'username': item.username,
                    'sex': userinfo.sex,
                    'name': userinfo.name,
                    'email': item.email,
                    'schoolnumber': userinfo.student_num,
                    'pass': 1,
                    'wealth': userinfo.money,
                }
            reslist.append(_dict)
        res = {
            'code': 0,
            'msg': "返回成功",
            'data': reslist,
               }
        response.write(json.dumps(res))
        return response


@check_admin_login
def table_doing(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_doing.html')
    if request.method == 'POST':
        response = HttpResponse()
        res = {}
        itemlist = []
        tables = TableDeal.objects.filter(isActive=1)
        for table in tables:
            user = User.objects.get(id=table.User_request_id)
            tableinfo = WorkTable.objects.get(id=table.Table_id)
            if not tableinfo.isAccept:
                pass
            elif not tableinfo.isFinished:
                _dict = {
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
                itemlist.append(_dict)
        res = {
            'code': 0,
            'msg': '成功',
            'data': itemlist
        }
        response.write(json.dumps(res, cls=ComplexEncoder))
        return response


@check_admin_login
def table_finish(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_finish.html')
    if request.method == 'POST':
        response = HttpResponse()
        res = {}
        itemlist = []
        tables = TableDeal.objects.filter(isActive=1)
        for table in tables:
            user = User.objects.get(id=table.User_request_id)
            tableinfo = WorkTable.objects.get(id=table.Table_id)
            username_runner = '无'
            username_runner_id = table.User_receive_id
            if username_runner_id:
                username_runner = User.objects.get(id=username_runner_id).username
            if tableinfo.isFinished:
                _dict = {
                    'title': tableinfo.title,
                    'goods': tableinfo.goods,
                    'classify': tableinfo.classify,
                    'phone': tableinfo.phone,
                    'username': user.username,
                    'reward': tableinfo.back,
                    'runner': username_runner,
                    'get_address': tableinfo.get_address,
                    'home_address': tableinfo.home_address,
                    'date_start': tableinfo.date_start+datetime.timedelta(hours=8),
                    'date_end': tableinfo.date_ending+datetime.timedelta(hours=8),
                    'describe': tableinfo.describe,
                }
                itemlist.append(_dict)
        res = {
            'code': 0,
            'msg': '成功',
            'data': itemlist
        }
        response.write(json.dumps(res, cls=ComplexEncoder))
        return response


@check_admin_login
def table_waiting(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_waiting.html')
    if request.method == 'POST':
        response = HttpResponse()
        res = {}
        itemlist = []
        tables = TableDeal.objects.filter(isActive=1)
        for table in tables:
            user = User.objects.get(id=table.User_request_id)
            tableinfo = WorkTable.objects.get(id=table.Table_id)
            if not tableinfo.isAccept:
                _dict = {
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
                itemlist.append(_dict)
        res = {
            'code': 0,
            'msg': '成功',
            'data': itemlist
        }
        response.write(json.dumps(res, cls=ComplexEncoder))
        return response


@check_admin_login
def update_user(request):
    if request.method == 'POST':
        post_dict = request.POST
        user_id = post_dict['user_id']
        username = post_dict['username']
        sex = post_dict['sex']
        name = post_dict['name']
        email = post_dict['email']
        stu_num = post_dict['stu_num']
        money = post_dict['money']
        user = User.objects.get(id=user_id)
        if not user:
            res = {
                'code': 0,
                'msg': '没有该用户，怎么回事呢',
            }
            return HttpResponse(json.dumps(res))
        userinfo_id = user.userinfo_id
        userinfo = UserInfo.objects.get(id=userinfo_id)
        if not userinfo:
            res = {
                'code': -1,
                'msg': '该用户没有完善信息，怎么回事呢',
            }
            return HttpResponse(json.dumps(res))
        user.username = username
        user.email = email
        userinfo.sex = sex
        userinfo.name = name
        userinfo.student_num = stu_num
        userinfo.money = money
        user.save()
        userinfo.save()
        res = {
            'code': 1,
            'msg': '成功'
        }
        return HttpResponse(json.dumps(res))


@check_admin_login
def delete_user(request):
    if request.method == 'POST':
        delete_user_id = request.POST['user_id']
        user = User.objects.get(id=delete_user_id)
        if not user:
            res = {
                'code': 0
            }
            return HttpResponse(json.dumps(res))
        else:
            user.is_active = 0;
            user.save()
            res = {
                'code':1
            }
            return HttpResponse(json.dumps(res))


@check_admin_login
def user_setting(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-setting.html')


@check_admin_login
def user_password(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-password.html')
    if request.method == 'POST':
        post_dict = request.POST
        password_old = post_dict['password_old']
        password_new = post_dict['password_new']


@check_admin_login
def user_search(request):
    if request.method == 'POST':
        post_dict = request.POST
        username = post_dict['username']
        sex = post_dict['sex']
        name = post_dict['name']
        stu_num = post_dict['stu_num']
        user_list = []
        users = User.objects.filter(is_active=1)
        if username:
            user = User.objects.get(username=username)
            if user:
                if user.userinfo_id:
                    userinfo = UserInfo.objects.get(id=user.userinfo_id)
                    _dict = {
                        'user_id': user.id,
                        'username': user.username,
                        'sex': userinfo.sex,
                        'name': userinfo.name,
                        'email': user.email,
                        'schoolnumber': userinfo.student_num,
                        'pass': 0,
                        'wealth': userinfo.money,
                        }
                    user_list.append(_dict)
                else:
                    _dict = {
                        'user_id': user.id,
                        'username': user.username,
                        'sex': "",
                        'name': '',
                        'email': user.email,
                        'schoolnumber': '',
                        'pass': 0,
                        'wealth': 0,
                    }
                    user_list.append(_dict)
        elif name:
            for user in users:
                if user.userinfo_id:
                    userinfo = UserInfo.objects.get(id=user.userinfo_id)
                    if userinfo:
                        if userinfo.name == name:
                            _dict = {
                                'user_id': user.id,
                                'username': user.username,
                                'sex': userinfo.sex,
                                'name': userinfo.name,
                                'email': user.email,
                                'schoolnumber': userinfo.student_num,
                                'pass': 0,
                                'wealth': userinfo.money,
                            }
                            user_list.append(_dict)
        elif sex:
            for user in users:
                if user.userinfo_id:
                    userinfo = UserInfo.objects.get(id=user.userinfo_id)
                    if userinfo:
                        if userinfo.sex == sex:
                            _dict = {
                                'user_id': user.id,
                                'username': user.username,
                                'sex': userinfo.sex,
                                'name': userinfo.name,
                                'email': user.email,
                                'schoolnumber': userinfo.student_num,
                                'pass': 0,
                                'wealth': userinfo.money,
                            }
                            user_list.append(_dict)
        elif stu_num:
            for user in users:
                if user.userinfo_id:
                    userinfo = UserInfo.objects.get(id=user.userinfo_id)
                    if userinfo:
                        if userinfo.student_num == stu_num:
                            _dict = {
                                'user_id': user.id,
                                'username': user.username,
                                'sex': userinfo.sex,
                                'name': userinfo.name,
                                'email': user.email,
                                'schoolnumber': userinfo.student_num,
                                'pass': 0,
                                'wealth': userinfo.money,
                            }
                            user_list.append(_dict)
        res = {
            'code': 0,
            'msg': '成功',
            'data': user_list,
        }
        return HttpResponse(json.dumps(res))


@check_admin_login
def editor(request):
    if request.method == 'GET':
        return render(request, 'admin/page/editor.html')
