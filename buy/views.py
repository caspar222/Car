import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


# 车辆品牌列表相关
from userinfo.models import Users
from .models import Cart, Orders
from sale.models import Carinfo
from sale.models import Brand


def brandlist(request):
    # 接受传递过来的 brand 信息
    brand = request.GET['brand']
    try:
        # 查询所有的品牌列表
        brand_list = Brand.objects.all()
        # 通过 品牌名称 获取品牌对象
        brand = Brand.objects.get(btitle=brand)
        # 查询 brand 下所有的车辆信息
        car_list = brand.carinfo_set.filter(ispurchase=0,isdelete=0)
        # 将要传递给模板的变量封装到字典中
        params = {
            'brand':brand,
            'car_list':car_list,
            'brand_list':brand_list,
        }
    except ObjectDoesNotExist as e:
        return HttpResponse(e)

    return render(request,'list.html',params)


def add_order(request):
    # 先验证用户是否登录过
    if request.user.is_authenticated():
        car_id = request.GET['carid']
        try:
            car = Carinfo.objects.get(id=car_id)
            brand = str(car.serbran) + car.ctitle
            picture = car.picture
            price = car.extractprice
            newprice = car.newprice
            mileage = car.mileage

            Cart.objects.create(suser=request.user,car=car,brand=brand,picture=picture,price=price,newprice=newprice,mileage=mileage)

        except ObjectDoesNotExist as e:
            return HttpResponse(e)
        return render(request,'order.html',{'car':locals()})

    else:
        return redirect('/user/login/')

# 将指定的车辆从购物车中删除出去
def del_order(request):
    users_id = request.user.id
    car_id = request.GET['carid']
    
    try:
        Cart.objects.filter(suser_id=users_id,car_id=car_id).delete()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)
    return redirect('/')


def confirmbuy(request):
    if request.user.is_authenticated():
        car_id = request.GET['carid']
        orderNO = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        cart = Cart.objects.filter(car_id=car_id)[0]
        car = Carinfo.objects.filter(id=car_id)[0]

        brand = cart.brand
        picture = cart.picture
        price = cart.price
        newprice = cart.newprice
        mileage = cart.mileage

        sale_user = car.user
        buy_user = request.user

        Orders.objects.create(sale_user=sale_user,buy_user=buy_user,brand=brand,picture=picture,price=price,newprice=newprice,mileage=mileage,orderno=orderNO)

        user_id = request.user.id
        #查询当前登录用户的所有订单
        orders = Orders.objects.filter(buy_user=user_id).order_by("-id")
        #查询当前登录用户信息
        user = Users.objects.get(id=user_id)
        #查询当前登录用户所卖的车
        car = Carinfo.objects.filter(user_id=user_id,ispurchase=0,isdelete=0)

        return render(request,'user-info.html',{'orders':locals()})

    else:
        return redirect('/user/login/')






