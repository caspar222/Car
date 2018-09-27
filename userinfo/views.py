from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from sale.models import Brand, Carinfo
from userinfo.models import *

# Create your views here.

auth_check = 'MarcelArhut'

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        user = auth.authenticate(username=username,password=password)

        if user is not None and user.is_active:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request,'login.html',{'errMsg':'用户名或密码不正确'})

def logout(request):
    auth.logout(request)
    return redirect('/')

# 声明一个全局的 new_user 对象，用于表示要注册的用户信息
new_user = Users()

def register(request):
    if request.method == 'GET':
        # 查看注册页面
        return render(request,'register.html')
    else:

        # 接收用户名和密码
        new_user.username = request.POST['username']
        # 判断用户名称是否存在
        oldUser = Users.objects.filter(username=new_user.username)

        if len(oldUser) > 0 :
            return render(request,'register.html',{'message':'用户名已经存在'})

        # 处理密码,调用django中的密码加密处理程序
        new_user.password = make_password(request.POST['userpwd'],auth_check,'pbkdf2_sha1')

        # 根据用户点击的按钮去往不同的页面
        if 'tobuy' in request.POST:
            return render(request,'buyregister.html')
        if 'tosale' in request.POST:
            return render(request,'info-message.html')

def buyinfo(request):
    # 继续向new_user中追加注册信息，再将new_user保存回数据库
    if request.method == 'POST':
        new_user.realname = request.POST['realname']
        new_user.uidentity = request.POST['identity']
        new_user.address = request.POST['address']
        new_user.cellphone = request.POST['phone']
        new_user.sex = request.POST['gender']
    try:
        new_user.save()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)
    return redirect('/')

# 我要卖车的注册行为
def infomes(request):
    if request.method == 'POST':
        # 获取用户信息插入到 Users 表中,继续向new_user中增加数据
        new_user.realname = request.POST['realname']
        new_user.uidentity = request.POST['identity']
        new_user.address = request.POST['address']
        new_user.cellphone = request.POST['phone']
        new_user.sex = request.POST['gender']
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            return HttpResponse(e)
        # 获取车辆信息插入到 Carinfo 表中
        # 获取车辆品牌
        brand = Brand.objects.filter(btitle=request.POST['brands'])[0]
        #创建Carinfo对象，并获取前端的值赋值给该对象
        car = Carinfo()
        car.ctitle = request.POST['model']
        car.regist_date = request.POST['regist_date']
        car.engineno = request.POST['engineNo']
        car.mileage = request.POST['mileage']
        car.maintenance_record = request.POST['isService']
        car.price = request.POST['price']
        car.extractprice = int(car.price)*0.02 + int(car.price)
        car.newprice = request.POST['newprice']
        # request.FILES['图片框name'] 获取上传文件
        car.picture = request.FILES['pic']
        car.formalities = request.POST['formalities']
        car.debt = request.POST['isDebt']
        car.promise = request.POST['promise']
        car.serbran = brand
        car.user = new_user
        try:
            car.save()
        except ObjectDoesNotExist as e:
            return HttpResponse(e)
        return redirect('/')










