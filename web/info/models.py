from django.db import models


class MonitorTask(models.Model):
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=2000)
    type = models.IntegerField(default=0)
    last_scan_time = models.DateTimeField(auto_now=True)
    wait_time = models.IntegerField(default=600)
    flag = models.CharField(max_length=2000, null=True, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'botend_monitortask'


class TargetAuth(models.Model):
    domain = models.CharField(max_length=200)
    cookie = models.TextField(null=True)
    is_login = models.BooleanField(default=True)
    ext = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        managed = False
        db_table = 'botend_targetauth'


class MonitorWebhook(models.Model):
    task_id = models.IntegerField()
    task_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'botend_monitorwebhook'


class WechatAccountTask(models.Model):
    biz = models.CharField(max_length=50)
    account = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=500, null=True)
    last_publish_time = models.DateTimeField(auto_now=True, null=True)
    last_spider_time = models.DateTimeField(auto_now=True, null=True)
    is_zombie = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'botend_wechataccounttask'


class WechatArticle(models.Model):
    account = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, default=None, null=True)
    url = models.CharField(max_length=255, default=None, null=True)
    author = models.CharField(max_length=255, default=None, null=True)
    publish_time = models.DateTimeField(default=None, null=True)
    biz = models.CharField(max_length=50)
    digest = models.CharField(max_length=255, default=None, null=True)
    cover = models.CharField(max_length=255, default=None, null=True)
    content_html = models.TextField(default=None, null=True)
    source_url = models.CharField(max_length=255, default=None, null=True)
    sn = models.CharField(unique=True, max_length=50, default=None, null=True)
    state = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'botend_wechatarticle'


class VulnMonitorTask(models.Model):
    task_name = models.CharField(max_length=255)
    target = models.CharField(max_length=1000, null=True)
    last_spider_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'botend_vulnmonitortask'


class VulnData(models.Model):
    sid = models.CharField(max_length=200, null=True)
    cveid = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100, null=True)
    score = models.CharField(max_length=10, default="0")
    severity = models.IntegerField(default=0)
    publish_time = models.DateTimeField()
    link = models.CharField(max_length=1000, null=True)
    description = models.TextField(null=True)
    solutions = models.TextField(null=True)
    source = models.CharField(max_length=1000, null=True)
    reference = models.CharField(max_length=1000, null=True)
    tag = models.CharField(max_length=200, null=True)
    is_poc = models.BooleanField(default=False)
    is_exp = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    state = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'botend_vulndata'
