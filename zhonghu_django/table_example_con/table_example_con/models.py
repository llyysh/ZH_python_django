from django.db import models

class ReconciliationUpstream(models.Model):
    """上游对账统计结果表"""
    processing_time = models.DateTimeField(auto_now_add=True)  # 处理时间
    month = models.CharField(max_length=6)  # 月份(如2502)
    upstream = models.CharField(max_length=100)  # 上游
    interface = models.CharField(max_length=200)  # 接口
    isp = models.CharField(max_length=50)  # 运营商
    price = models.DecimalField(max_digits=10, decimal_places=5)  # 单价
    count = models.IntegerField()  # 数量

    class Meta:
        db_table = "reconciliation_upstream"

class ReconciliationDownstream(models.Model):
    """下游客户对账统计结果表"""
    processing_time = models.DateTimeField(auto_now_add=True)  # 处理时间
    month = models.CharField(max_length=6)  # 月份(如2502)
    user = models.CharField(max_length=100)  # 用户
    interface = models.CharField(max_length=200)  # 接口
    isp = models.CharField(max_length=50)  # 运营商
    price = models.DecimalField(max_digits=10, decimal_places=5)  # 单价
    count = models.IntegerField()  # 数量

    class Meta:
        db_table = "reconciliation_downstream"