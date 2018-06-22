from django.db import models

# Create your models here.
from django.db.models import CharField, TextField, IntegerField, DecimalField


# 用户表
class User(models.Model):
    # 用户名
    user_name = CharField(max_length=50)
    # 手机号
    user_phone = CharField(max_length=20)
    # 登陆密码
    user_password = CharField(max_length=50)
    # 第一张人脸
    user_face_0 = TextField()
    # 第二张人脸
    user_face_1 = TextField()
    # 第三张人脸
    user_face_2 = TextField()
    # 第四张人脸
    user_face_3 = TextField()
    # 第五张人脸
    user_face_4 = TextField()
    # 余额
    balance = DecimalField(max_digits=15, decimal_places=2)

    pass


# 活动表
class Activity(models.Model):
    # 付款电话号码
    a_user_phone = CharField(max_length=20, default='')
    # 收款电话号码
    b_user_phone = CharField(max_length=20, default='')
    # 状态
    status = CharField(max_length=50)
    # 转账金额
    money = DecimalField(max_digits=15, decimal_places=2)
    pass
