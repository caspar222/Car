from django.db import models

# Create your models here.
from userinfo.models import Users


class Brand(models.Model):
    logo_brand = models.CharField(max_length=100)
    btitle = models.CharField(max_length=30)
    isdelete = models.IntegerField(db_column='isDelete')  # Field name made lowercase.

    def __str__(self):
        return self.btitle

    class Meta:
        managed = False
        db_table = 'Brand'


class Carinfo(models.Model):
    # 车名
    ctitle = models.CharField(max_length=30)
    # 上牌日期
    regist_date = models.DateField()
    # 发动机号
    engineno = models.CharField(db_column='engineNo', max_length=30)  # Field name made lowercase.
    # 公里数
    mileage = models.IntegerField()
    # 维修记录
    maintenance_record = models.CharField(max_length=10)
    # 期望售价
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # 成交价格
    extractprice = models.DecimalField(max_digits=8, decimal_places=2)
    # 新车价格
    newprice = models.DecimalField(max_digits=8, decimal_places=2)
    # 照片 - 需要将 CharField更改为ImageField
    picture = models.ImageField(upload_to='img/car',max_length=100)
    # 手续
    formalities = models.CharField(max_length=10)
    # 债务
    debt = models.CharField(max_length=10)
    #　卖家承诺
    promise = models.TextField(blank=True, null=True)
    # 审核进度
    examine = models.CharField(max_length=30)
    # 是否成交 - 增加默认值 default=0
    ispurchase = models.IntegerField(db_column='isPurchase',default=0)  # Field name made lowercase.
    # 车辆型号
    serbran = models.ForeignKey(Brand, models.DO_NOTHING)
    # 用户
    user = models.ForeignKey(Users, models.DO_NOTHING)
    # 是否删除 - 增加默认值 default=0
    isdelete = models.IntegerField(db_column='isDelete',default=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Carinfo'