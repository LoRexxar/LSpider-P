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
from web.info.controller import wechat, vuln, rss


app_name = "info"

urlpatterns = [
    path("", views.index),

    # project
    path("wechat", csrf_exempt(wechat.WechatAccountListView.as_view()), name="wechat"),
    path("wechat/count", csrf_exempt(wechat.WechatAccountCountView.as_view()), name="wechat_count"),
    path("wechat/<int:account_id>", csrf_exempt(wechat.WechatAccountDetailsView.as_view()), name="wechat_detail"),

    path("wechat/article", csrf_exempt(wechat.WechatArticleListView.as_view()), name="wechat_article"),
    path("wechat/article/count", csrf_exempt(wechat.WechatArticleCountView.as_view()), name="wechat_article_count"),
    path("wechat/article/<int:art_id>", csrf_exempt(wechat.WechatArticleDetailsView.as_view()), name="wechat_article_detail"),

    path("monitor/task", csrf_exempt(wechat.MonitorTaskListView.as_view()), name="wechat_task"),
    path("monitor/task/count", csrf_exempt(wechat.MonitorTaskCountView.as_view()), name="wechat_task_count"),
    path("monitor/task/<int:task_id>", csrf_exempt(wechat.MonitorTaskDetailsView.as_view()), name="wechat_task_detail"),

    path("monitor/auth", csrf_exempt(wechat.TargetAuthListView.as_view()), name="wechat_profile"),
    path("monitor/auth/<int:auth_id>", csrf_exempt(wechat.TargetAuthDetailsView.as_view()), name="wechat_profile_detail"),

    path("vuln/task", csrf_exempt(vuln.VulnMonitorTaskListView.as_view()), name="vuln_task"),
    path("vuln/task/count", csrf_exempt(vuln.VulnMonitorTaskCountView.as_view()), name="vuln_task_count"),
    path("vuln/task/<int:task_id>", csrf_exempt(vuln.VulnMonitorTaskDetailsView.as_view()), name="vuln_task_detail"),

    path("vuln/", csrf_exempt(vuln.VulnDataListView.as_view()), name="vuln_list"),
    path("vuln/count", csrf_exempt(vuln.VulnDataCountView.as_view()), name="vuln_task_count"),
    path("vuln/<int:vid>", csrf_exempt(vuln.VulnDataDetailsView.as_view()), name="vuln_detail"),

    path("rss/task", csrf_exempt(rss.RssMonitorTaskListView.as_view()), name="rss_task"),
    path("rss/task/count", csrf_exempt(rss.RssMonitorTaskCountView.as_view()), name="rss_task_count"),
    path("rss/task/<int:task_id>", csrf_exempt(rss.RssMonitorTaskDetailsView.as_view()), name="rss_task_detail"),

    path("rss/", csrf_exempt(rss.RssArticleListView.as_view()), name="rss_list"),
    path("rss/count", csrf_exempt(rss.RssArticleCountView.as_view()), name="rss_task_count"),
    path("rss/<int:vid>", csrf_exempt(rss.RssArticleDetailsView.as_view()), name="rss_detail"),
]
