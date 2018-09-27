from django.conf.urls import url
from buy import views
urlpatterns = [
    # 访问路径是　/buy/brandlist 交给　brandlist 视图处理
    url(r'^brandlist/$',views.brandlist,name='brandlist'),
    url(r'^addorder/$',views.add_order,name='addorder'),
    url(r'^delcart/$',views.del_order,name='delcart'),
    url(r'^confirmbuy/$',views.confirmbuy,name='confirmbuy'),
]