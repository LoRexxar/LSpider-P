#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: wechat.py
@time: 2023/4/3 18:46
@desc:

'''

from __future__ import unicode_literals

import json

from django.views import View
from django.http import HttpResponse, JsonResponse

from utils.base import check_gpc_undefined
from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required
from web.info.models import WechatAccountTask, WechatArticle, TargetAuth, MonitorTask


class WechatAccountListView(View):
    """
        公众号列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        account = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "account" in request.GET:
            account = request.GET['account'].strip()

        if account:
            was = WechatAccountTask.objects.filter(account__contains=account).using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        else:
            was = WechatAccountTask.objects.all().using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        count = len(was)

        return JsonResponse({"code": 200, "status": True, "message": list(was), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        biz = check_gpc_undefined(params, "biz")
        account = check_gpc_undefined(params, "account")
        summary = check_gpc_undefined(params, "summary")
        last_publish_time = check_gpc_undefined(params, "last_publish_time")
        last_spider_time = check_gpc_undefined(params, "last_spider_time")
        is_zombie = check_gpc_undefined(params, "is_zombie", 0)

        wa = WechatAccountTask(field_biz=biz, account=account, summary=summary, last_publish_time=last_publish_time, last_spider_time=last_spider_time, is_zombie=is_zombie)
        wa.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class WechatAccountCountView(View):
    """
        公众号列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        account = ""

        if "account" in request.GET:
            account = request.GET['account']

        if type:
            count = WechatAccountTask.objects.filter(account__contains=account).using("lmonitor").count()
        else:
            count = WechatAccountTask.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class WechatAccountDetailsView(View):
    """
        公众号详情
    """

    @staticmethod
    @login_level4_required
    def get(request, account_id):

        wa = WechatAccountTask.objects.filter(id=account_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wa)})

    @staticmethod
    @login_level4_required
    def post(request, account_id):
        params = json.loads(request.body)

        wa = WechatAccountTask.objects.filter(id=account_id).using("lmonitor").first()

        biz = check_gpc_undefined(params, "biz")
        account = check_gpc_undefined(params, "account")
        summary = check_gpc_undefined(params, "summary")
        last_publish_time = check_gpc_undefined(params, "last_publish_time")
        last_spider_time = check_gpc_undefined(params, "last_spider_time")
        is_zombie = check_gpc_undefined(params, "is_zombie", 0)

        if wa:
            wa.field_biz = biz
            wa.account = account
            wa.summary = summary
            wa.last_publish_time = last_publish_time
            wa.last_spider_time = last_spider_time
            wa.is_zombie = is_zombie
            wa.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Account not found"})


class MonitorTaskListView(View):
    """
        监控任务列表
    """

    @staticmethod
    @login_level4_required
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
            mts = MonitorTask.objects.filter(name__contains=name).using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        else:
            mts = MonitorTask.objects.all().using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        count = len(mts)

        return JsonResponse({"code": 200, "status": True, "message": list(mts), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        name = check_gpc_undefined(params, "name")
        target = check_gpc_undefined(params, "target")
        mtype = check_gpc_undefined(params, "type")
        last_scan_time = check_gpc_undefined(params, "last_scan_time")
        flag = check_gpc_undefined(params, "flag")
        wait_time = check_gpc_undefined(params, "wait_time")
        is_active = check_gpc_undefined(params, "is_active", 0)

        mt = MonitorTask(name=name, target=target, type=mtype, last_scan_time=last_scan_time, flag=flag, wait_time=wait_time, is_active=is_active)
        mt.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class MonitorTaskCountView(View):
    """
        监控任务统计
    """

    @staticmethod
    @login_level4_required
    def get(request):
        name = ""

        if "name" in request.GET:
            name = request.GET['name']

        if type:
            count = MonitorTask.objects.filter(name__contains=name).using("lmonitor").count()
        else:
            count = MonitorTask.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class MonitorTaskDetailsView(View):
    """
        监控任务详情
    """

    @staticmethod
    @login_level4_required
    def get(request, task_id):

        mt = MonitorTask.objects.filter(id=task_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(mt)})

    @staticmethod
    @login_level4_required
    def post(request, task_id):
        params = json.loads(request.body)

        mt = MonitorTask.objects.filter(id=task_id).using("lmonitor").first()

        name = check_gpc_undefined(params, "name")
        target = check_gpc_undefined(params, "target")
        mtype = check_gpc_undefined(params, "type")
        last_scan_time = check_gpc_undefined(params, "last_scan_time")
        flag = check_gpc_undefined(params, "flag")
        wait_time = check_gpc_undefined(params, "wait_time")
        is_active = check_gpc_undefined(params, "is_active", 0)

        if mt:
            mt.name = name
            mt.target = target
            mt.mtype = mtype
            mt.last_scan_time = last_scan_time
            mt.flag = flag
            mt.wait_time = wait_time
            mt.is_active = is_active
            mt.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Account not found"})


class WechatArticleListView(View):
    """
        公众号文章列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        title = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "title" in request.GET:
            title = request.GET['title'].strip()

        if title:
            warts = WechatArticle.objects.filter(title__contains=title).using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        else:
            warts = WechatArticle.objects.all().using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        count = len(warts)

        return JsonResponse({"code": 200, "status": True, "message": list(warts), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        account = check_gpc_undefined(params, "account")
        title = check_gpc_undefined(params, "title")
        url = check_gpc_undefined(params, "url")
        author = check_gpc_undefined(params, "author")
        publish_time = check_gpc_undefined(params, "publish_time")
        biz = check_gpc_undefined(params, "biz")
        digest = check_gpc_undefined(params, "digest")
        cover = check_gpc_undefined(params, "cover")
        content_html = check_gpc_undefined(params, "content_html")
        source_url = check_gpc_undefined(params, "source_url")
        sn = check_gpc_undefined(params, "sn")
        state = check_gpc_undefined(params, "state")

        wart = WechatArticle(field_biz=biz, account=account, title=title, url=url, author=author,
                             publish_time=publish_time, digest=digest, cover=cover,
                             content_html=content_html, source_url=source_url,
                             sn=sn, state=state)
        wart.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class WechatArticleCountView(View):
    """
        公众号文章列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        title = ""

        if "title" in request.GET:
            title = request.GET['title']

        if title:
            count = WechatArticle.objects.filter(title__contains=title).using("lmonitor").count()
        else:
            count = WechatArticle.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class WechatArticleDetailsView(View):
    """
        公众号文章详情
    """

    @staticmethod
    @login_level4_required
    def get(request, art_id):

        wart = WechatArticle.objects.filter(id=art_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wart)})

    @staticmethod
    @login_level4_required
    def post(request, art_id):
        params = json.loads(request.body)

        wart = WechatArticle.objects.filter(id=art_id).using("lmonitor").first()

        account = check_gpc_undefined(params, "account")
        title = check_gpc_undefined(params, "title")
        url = check_gpc_undefined(params, "url")
        author = check_gpc_undefined(params, "author")
        publish_time = check_gpc_undefined(params, "publish_time")
        biz = check_gpc_undefined(params, "biz")
        digest = check_gpc_undefined(params, "digest")
        cover = check_gpc_undefined(params, "cover")
        content_html = check_gpc_undefined(params, "content_html")
        source_url = check_gpc_undefined(params, "source_url")
        sn = check_gpc_undefined(params, "sn")
        state = check_gpc_undefined(params, "state")

        if wart:
            wart.field_biz = biz
            wart.account = account
            wart.title = title
            wart.url = url
            wart.author = author
            wart.publish_time = publish_time
            wart.digest = digest
            wart.cover = cover
            wart.content_html = content_html
            wart.source_url = source_url
            wart.sn = sn
            wart.state = state
            wart.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Article Task not found"})


class TargetAuthListView(View):
    """
        爬虫配置
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        tas = TargetAuth.objects.all().using("lmonitor").values()[::-1][(page - 1) * size:page * size]

        return JsonResponse({"code": 200, "status": True, "message": list(tas)})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        profile_name = check_gpc_undefined(params, "profile_name")
        value = check_gpc_undefined(params, "value")

        tas = TargetAuth(profile_name=profile_name, value=value)
        tas.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class TargetAuthDetailsView(View):
    """
        爬虫配置详情
    """

    @staticmethod
    @login_level4_required
    def get(request, auth_id):

        tas = TargetAuth.objects.filter(id=auth_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(tas)})

    @staticmethod
    @login_level4_required
    def post(request, auth_id):
        params = json.loads(request.body)

        ta = TargetAuth.objects.filter(id=auth_id).using("lmonitor").first()

        domain = check_gpc_undefined(params, "domain")
        cookie = check_gpc_undefined(params, "cookie")
        is_login = check_gpc_undefined(params, "is_login")
        ext = check_gpc_undefined(params, "ext")

        if ta:
            ta.profile_name = domain
            ta.cookie = cookie
            ta.is_login = is_login
            ta.ext = ext
            ta.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Profile not found"})
