from django.shortcuts import render
from django.http import HttpResponse
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


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')


def welcome(request):
    if request.method == 'GET':
        return render(request, 'admin/page/welcome.html')
    if request.method == 'POST':
        if request.POST['msg'] == 'get_info':
            response = HttpResponse()
            res = {}
            user_count = User.objects.count()
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


def table_user(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_user.html')
    if request.method == 'POST':
        response = HttpResponse()
        reslist = []
        Userlist = User.objects.all()
        for item in Userlist:
            print(item.userinfo_id)
            if not item.userinfo_id:
                _dict = {
                    'username': item.username,
                    'sex': "",
                    'name': '',
                    'email': item.email,
                    'schoolnumber': '',
                    'pass': 1,
                    'wealth': 0,
                }
            else:
                userinfo = UserInfo.objects.get(id=item.userinfo_id)
                _dict = {
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
            'code':0,
            'msg':"返回成功",
            'data':reslist,
               }
        response.write(json.dumps(res))
        return response


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


def user_setting(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-setting.html')


def user_password(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-password.html')


def editor(request):
    if request.method == 'GET':
        return render(request, 'admin/page/editor.html')



