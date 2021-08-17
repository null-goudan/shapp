from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户信息表
class UserInfo(models.Model):
    """
    用户信息表
    """
    name = models.CharField('姓名', max_length=15, default=None)
    sex = models.CharField('性别', max_length=10, default='男')
    age = models.IntegerField('年龄', default=0)
    student_num = models.CharField('学号', max_length=32, default='')
    student_class = models.CharField('学生班级', max_length=32, default='')
    score = models.IntegerField('积分', default=0)
    money = models.IntegerField('余额', default=0)


class User(AbstractUser):
    """
    继承自Django的内置用户表
    新加指向用户信息表的外键
    """
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class WorkTable(models.Model):
    """
    单子表：
    储存单子的信息
    """
    title = models.CharField('单子标题', max_length=32, default='')
    context = models.TextField('单子需求', max_length=500, default='')
    back = models.IntegerField('回报', default=0)
    BackType = models.BooleanField('回报类型', default=False)  # 0代表金钱 1代表积分
    TableType = models.CharField('单子类型', max_length=32,default='未知')
    isAccept = models.BooleanField('是否已经接单', default=False)
    isFinished = models.BooleanField('是否结束', default=False)


class TableDeal(models.Model):
    """
    图里面没有的一个部分，我发现需要单独建立出来一个表来表示这个交易信息,相当于上次那个比分表
    交易信息表
    """
    User_request = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_request')  # 需求方，发布单子的用户
    User_receive = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_receive')  # 接收方，接受单子的用户
    isActive = models.BooleanField(default=False)   # 方便删除
    Table = models.ForeignKey(WorkTable, on_delete=models.CASCADE)  # 指向表的信息
