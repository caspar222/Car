from django.conf.urls import url
from sale import views
urlpatterns = [
    # 当访问路径是　/sale/detail 的时候
    url(r'^detail/$',views.detail,name='detail'),
    url(r'^price0_10/$',views.price0_10,name='price0_10'),
    url(r'^price10_30/$',views.price10_30,name='price10_30'),
    url(r'^price30_80/$',views.price30_80,name='price30_80'),
    url(r'^price80_/$',views.price80_,name='price80_')
]