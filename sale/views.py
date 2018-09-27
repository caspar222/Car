from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import random
# Create your views here.

# 首页展示的视图处理函数
# 匹配路径：/
def index(request):
    # 查询所有的品牌信息
    brand_list = Brand.objects.filter(isdelete=0).order_by('-id')
    # 查询所有的热卖车型：查询所有待卖车辆，取出随机５条记录
    car_list = Carinfo.objects.filter(ispurchase=0,isdelete=0)
    car_five = random.sample(list(car_list),5)

    # 允许将变量封装到字典上再传递给首页
    # dic = {
    #     "bList":brand_list,
    # }
    return render(request,'index.html',locals())


#查看汽车详情的处理视图
# /sale/detail/?carid=xx
def detail(request):
    # 接收前端传递过来的carid
    carid = request.GET['carid']

    try:
        # 根据 carid 查询出对应的车辆的信息
        car = Carinfo.objects.get(id=carid)
    except ObjectDoesNotExist as e:
        return HttpResponse(e)

    #处理最近浏览
    if request.COOKIES.get('Recently_Viewed',''):
        #cookies中有最近浏览的信息 : 36,72
        cookie_car = request.COOKIES.get('Recently_Viewed')
        list_car = cookie_car.split(',')
        print(list_car)
        # 如果 list_car中已经有了carid，则将其删除
        if carid in list_car:
            list_car.remove(carid)
        # 判断浏览记录的数量是否大于等于2
        if len(list_car) >= 2:
            list_car.pop()

        list_car = [carid] + list_car
        cookie_car_new = ','.join(list_car)
    else:
        #cookies中没有最近浏览的信息
        cookie_car_new = carid

    resp = render(request,'detail.html',{'car':car})
    resp.set_cookie('Recently_Viewed',cookie_car_new,60*60)
    return resp





# 根据价格区间查询车辆信息，由视图处理函数来调用
# request : 对应的请求对象，由视图处理函数传递进来
# priceLow : 区间的最低价
# priceHigh : 区间的最高价
def price_car(request,priceLow,priceHigh=None):
    brand = request.GET['brand']
    if brand == 'None':
        if priceHigh:
            car_list = Carinfo.objects.filter(ispurchase=0,isdelete=0,price__gt=priceLow,price__lt=priceHigh)
        else:
            car_list = Carinfo.objects.filter(ispurchase=0,isdelete=0,price__gt=priceLow)
    else:
        brand = Brand.objects.get(btitle=brand)
        if priceHigh:
            car_list = brand.carinfo_set.filter(ispurchase=0,isdelete=0,price__gt=priceLow,price__lt=priceHigh)
        else:
            car_list = brand.carinfo_set.filter(ispurchase=0, isdelete=0, price__gt=priceLow)

    brand_list = Brand.objects.all()

    params = {
        'brand':brand,
        'car_list':car_list,
        'brand_list':brand_list,
    }
    resp = render(request,'list.html',params)
    return resp

# 按价格区间查看车辆信息
# 访问路径是:http://localhsot:8000/sale/price0_10 ，则在所有的车辆中筛选出0-10W的车
# 访问路径是:http://localhost:8000/sale/price0_10/?brand=xxx,则在xxx品牌下筛选0-10W的车
def price0_10(request):
    return price_car(request,0,10)

# 按价格区间查看车辆信息

# 访问路径是:http://localhost:8000/sale/price10_30/?brand=None 的时候，则在所有车辆中筛选出10-30W的车

# 访问路径是:http://localhost:8000/sale/price10_30/?brand=xxx 的时候，则在xxx品牌下筛选10-30W的车
def price10_30(request):
    return price_car(request,10,30)

# 按价格区间查看车辆信息

# 访问路径是:http://localhost:8000/sale/price30_80/?brand=None 的时候，则在所有车辆中筛选出30-80W的车

# 访问路径是:http://localhost:8000/sale/price30_80/?brand=xxx 的时候，则在xxx品牌下筛选30-80W的车
def price30_80(request):
    return price_car(request,30,80)


def price80_(request):
    return price_car(request,80)









