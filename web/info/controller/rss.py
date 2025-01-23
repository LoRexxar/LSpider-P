#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: rss.py
@time: 2023/6/19 15:11
@desc:

'''


from __future__ import unicode_literals

import json
import pytz
import datetime

from django.views import View
from django.http import HttpResponse, JsonResponse

from utils.base import check_gpc_undefined
from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required
from web.info.models import RssArticle, RssMonitorTask


class RssMonitorTaskListView(View):
    """
        rss监控列表
    """

    @staticmethod
    @login_level1_required
    def get(request):
        size = 10
        page = 1
        name = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "name" in request.GET:
            name = request.GET['name'].strip()

        if name:
            rmts = RssMonitorTask.objects.filter(name__contains=name).using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        else:
            rmts = RssMonitorTask.objects.all().using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        count = len(rmts)

        return JsonResponse({"code": 200, "status": True, "message": list(rmts), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        name = check_gpc_undefined(params, "name")
        link = check_gpc_undefined(params, "link")
        tag = check_gpc_undefined(params, "tag")
        is_active = check_gpc_undefined(params, "is_active", 1)

        rmt = RssMonitorTask(name=name, link=link, tag=tag, is_active=is_active)
        rmt.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class RssMonitorTaskCountView(View):
    """
        rss任务列表
    """

    @staticmethod
    @login_level1_required
    def get(request):
        name = ""

        if "name" in request.GET:
            name = request.GET['name']

        if type:
            count = RssMonitorTask.objects.filter(name__contains=name).using("lmonitor").count()
        else:
            count = RssMonitorTask.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class RssMonitorTaskDetailsView(View):
    """
        rss任务详情
    """

    @staticmethod
    @login_level1_required
    def get(request, task_id):

        rmts = RssMonitorTask.objects.filter(id=task_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(rmts)})

    @staticmethod
    @login_level4_required
    def post(request, task_id):
        params = json.loads(request.body)

        rmt = RssMonitorTask.objects.filter(id=task_id).using("lmonitor").first()

        name = check_gpc_undefined(params, "name")
        link = check_gpc_undefined(params, "link")
        tag = check_gpc_undefined(params, "tag")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if rmt:
            rmt.name = name
            rmt.link = link
            rmt.tag = tag
            rmt.is_active = is_active
            rmt.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "RssMonitor Task not found"})


class RssArticleListView(View):
    """
        rss列表
    """

    @staticmethod
    @login_level1_required
    def get(request):
        size = 10
        page = 1
        title = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "title" in request.GET:
            title = request.GET['title'].strip().lower()

        if title:
            ras = RssArticle.objects.filter(title__icontains=title, is_active=1).using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        else:
            ras = RssArticle.objects.filter(is_active=1).using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        count = len(ras)

        for ra in ras:
            ra['content_html'] = ra['content_html'][:150]+"..."

            local_tz = pytz.timezone('Asia/Shanghai')
            ra['publish_time'] = ra['publish_time'].replace(tzinfo=local_tz).strftime("%Y-%m-%d %H:%M:%S")

        return JsonResponse({"code": 200, "status": True, "message": list(ras), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        rss_id = check_gpc_undefined(params, "rss_id")
        title = check_gpc_undefined(params, "title")
        url = check_gpc_undefined(params, "url")
        author = check_gpc_undefined(params, "author")
        content_html = check_gpc_undefined(params, "content_html")
        is_active = check_gpc_undefined(params, "is_active", 1)

        ra = RssArticle(rss_id=rss_id, title=title, url=url, author=author, content_html=content_html, is_active=is_active)
        ra.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class RssArticleCountView(View):
    """
        rss列表
    """

    @staticmethod
    @login_level1_required
    def get(request):
        title = ""

        if "title" in request.GET:
            title = request.GET['title']

        if type:
            count = RssArticle.objects.filter(title__contains=title).using("lmonitor").count()
        else:
            count = RssArticle.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class RssArticleDetailsView(View):
    """
        rss详情
    """

    @staticmethod
    @login_level1_required
    def get(request, vid):

        ras = RssArticle.objects.filter(id=vid).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(ras)})

    @staticmethod
    @login_level4_required
    def post(request, vid):
        params = json.loads(request.body)

        ra = RssArticle.objects.filter(id=vid).using("lmonitor").first()

        rss_id = check_gpc_undefined(params, "rss_id")
        title = check_gpc_undefined(params, "title")
        url = check_gpc_undefined(params, "url")
        author = check_gpc_undefined(params, "author")
        content_html = check_gpc_undefined(params, "content_html")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if ra:
            ra.rss_id = rss_id
            ra.title = title
            ra.url = url
            ra.author = author
            ra.content_html = content_html
            ra.is_active = is_active
            ra.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "RssArticle not found"})
