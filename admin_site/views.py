from django.shortcuts import render
from django.http import HttpResponse
from model.models import User, TableDeal, UserInfo, WorkTable
import json


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
            table_list = TableDeal.objects.all()
            for item in table_list:
                if not item.User_receive_id:
                    table_waiting_count += 1
                else:
                    table_id = item.Table_id
                    tableinfo = WorkTable.objects.get(id=table_id)
                    if tableinfo.isAccept and not tableinfo.isFinished:
                        table_doing_count += 1
                    else:
                        table_finish_count += 1

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


def table_finish(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_finish.html')


def table_waiting(request):
    if request.method == 'GET':
        return render(request, 'admin/page/table_waiting.html')


def user_setting(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-setting.html')


def user_password(request):
    if request.method == 'GET':
        return render(request, 'admin/page/user-password.html')


def editor(request):
    if request.method == 'GET':
        return render(request, 'admin/page/editor.html')
