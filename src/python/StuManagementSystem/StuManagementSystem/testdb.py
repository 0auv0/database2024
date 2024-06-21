# -*- coding: utf-8 -*-

from django.http import HttpResponse

# from login.models import User
from basedb.models import Student

# 数据库操作
def testdb(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Student.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Student.objects.filter(sid="PB21111681")

    # 获取单个对象
    response3 = Student.objects.get(sid="PB21111681")

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    Student.objects.order_by('sid')[0:2]

    # 数据排序
    Student.objects.order_by("sid")

    # 上面的方法可以连锁使用
    Student.objects.filter(sname="朱炜荣").order_by("sid")

    # 输出所有数据
    for var in list:
        response1 += var.sname + " "
    response1 += "<br>"
    for var in response2:
        response1 += var.sname + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")