from django.db import models


class WechatAccount(models.Model):
    field_biz = models.CharField(db_column='__biz', unique=True, max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    account = models.CharField(max_length=255, blank=True, null=True)
    head_url = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=500, blank=True, null=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    verify = models.CharField(max_length=255, blank=True, null=True)
    spider_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wechat_account'


class WechatAccountTask(models.Model):
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    last_publish_time = models.DateTimeField(blank=True, null=True)
    last_spider_time = models.DateTimeField(blank=True, null=True)
    is_zombie = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wechat_account_task'


class WechatArticle(models.Model):
    account = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    digest = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    pics_url = models.TextField(blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)
    source_url = models.CharField(max_length=255, blank=True, null=True)
    comment_id = models.CharField(max_length=50, blank=True, null=True)
    sn = models.CharField(unique=True, max_length=50, blank=True, null=True)
    spider_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wechat_article'


class WechatArticleComment(models.Model):
    comment_id = models.CharField(max_length=50, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    content_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    is_top = models.IntegerField(blank=True, null=True)
    spider_time = models.DateTimeField(blank=True, null=True)
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'wechat_article_comment'


class WechatArticleDynamic(models.Model):
    sn = models.CharField(unique=True, max_length=50, blank=True, null=True)
    read_num = models.IntegerField(blank=True, null=True)
    like_num = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    spider_time = models.DateTimeField(blank=True, null=True)
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'wechat_article_dynamic'


class WechatArticleList(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    digest = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source_url = models.CharField(max_length=1000, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    subtype = models.IntegerField(blank=True, null=True)
    is_multi = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    copyright_stat = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    del_flag = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    sn = models.CharField(unique=True, max_length=50, blank=True, null=True)
    spider_time = models.DateTimeField(blank=True, null=True)
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'wechat_article_list'


class WechatArticleTask(models.Model):
    id = models.BigAutoField(primary_key=True)
    sn = models.CharField(unique=True, max_length=50, blank=True, null=True)
    article_url = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    field_biz = models.CharField(db_column='__biz', max_length=50, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'wechat_article_task'


class WechatProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile_name = models.CharField(max_length=100, null=True)
    value = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = 'wechat_profile'
