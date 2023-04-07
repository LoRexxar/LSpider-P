#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: urls.py
@time: 2023/4/6 15:39
@desc:

'''
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from web.info import views
from web.info.controller import wechat


app_name = "info"

urlpatterns = [
    path("", views.index),

    # project
    path("wechat", csrf_exempt(wechat.WechatAccountListView.as_view()), name="wechat"),
    path("wechat/count", csrf_exempt(wechat.WechatAccountCountView.as_view()), name="wechat_count"),
    path("wechat/<int:account_id>", csrf_exempt(wechat.WechatAccountDetailsView.as_view()), name="wechat_detail"),

    path("wechat/task", csrf_exempt(wechat.WechatAccountTaskListView.as_view()), name="wechat_task"),
    path("wechat/task/count", csrf_exempt(wechat.WechatAccountTaskCountView.as_view()),
         name="wechat_task_count"),
    path("wechat/task/<int:task_id>", csrf_exempt(wechat.WechatAccountTaskDetailsView.as_view()),
         name="wechat_task_detail"),

    path("wechat/article", csrf_exempt(wechat.WechatArticleListView.as_view()), name="wechat_article"),
    path("wechat/article/count", csrf_exempt(wechat.WechatArticleCountView.as_view()),
         name="wechat_article_count"),
    path("wechat/article/<int:art_id>", csrf_exempt(wechat.WechatArticleDetailsView.as_view()),
         name="wechat_article_detail"),
]
