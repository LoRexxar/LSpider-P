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
from web.info.models import WechatAccount, WechatAccountTask, WechatArticle, WechatProfile


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
            was = WechatAccount.objects.filter(account__contains=account).using("wechat").values()[::-1][(page - 1) * size:page * size]
        else:
            was = WechatAccount.objects.all().using("wechat").values()[::-1][(page - 1) * size:page * size]
        count = len(was)

        return JsonResponse({"code": 200, "status": True, "message": list(was), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        biz = check_gpc_undefined(params, "biz")
        account = check_gpc_undefined(params, "account")
        head_url = check_gpc_undefined(params, "head_url")
        summary = check_gpc_undefined(params, "summary")
        qr_code = check_gpc_undefined(params, "qr_code")
        verify = check_gpc_undefined(params, "verify")
        spider_time = check_gpc_undefined(params, "spider_time")

        wa = WechatAccount(field_biz=biz, account=account, head_url=head_url, summary=summary, qr_code=qr_code, verify=verify, spider_time=spider_time)
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
            count = WechatAccount.objects.filter(account__contains=account).using("wechat").count()
        else:
            count = WechatAccount.objects.all().using("wechat").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class WechatAccountDetailsView(View):
    """
        公众号详情
    """

    @staticmethod
    @login_level4_required
    def get(request, account_id):

        wa = WechatAccount.objects.filter(id=account_id).using("wechat").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wa)})

    @staticmethod
    @login_level4_required
    def post(request, account_id):
        params = json.loads(request.body)

        wa = WechatAccount.objects.filter(id=account_id).using("wechat").first()

        biz = check_gpc_undefined(params, "biz")
        account = check_gpc_undefined(params, "account")
        head_url = check_gpc_undefined(params, "head_url")
        summary = check_gpc_undefined(params, "summary")
        qr_code = check_gpc_undefined(params, "qr_code")
        verify = check_gpc_undefined(params, "verify")
        spider_time = check_gpc_undefined(params, "spider_time")

        if wa:
            wa.field_biz = biz
            wa.account = account
            wa.head_url = head_url
            wa.summary = summary
            wa.qr_code = qr_code
            wa.verify = verify
            wa.spider_time = spider_time
            wa.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Account not found"})


class WechatAccountTaskListView(View):
    """
        公众号扫描任务列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        biz = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "biz" in request.GET:
            biz = request.GET['biz'].strip()

        if biz:
            wats = WechatAccountTask.objects.filter(field_biz__contains=biz).using("wechat").values()[::-1][(page - 1) * size:page * size]
        else:
            wats = WechatAccountTask.objects.all().using("wechat").values()[::-1][(page - 1) * size:page * size]
        count = len(wats)

        return JsonResponse({"code": 200, "status": True, "message": list(wats), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        biz = check_gpc_undefined(params, "biz")
        is_zombie = check_gpc_undefined(params, "is_zombie", 0)

        wat = WechatAccountTask(field_biz=biz, is_zombie=is_zombie)
        wat.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class WechatAccountTaskCountView(View):
    """
        公众号任务列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        biz = ""

        if "biz" in request.GET:
            biz = request.GET['biz']

        if type:
            count = WechatAccountTask.objects.filter(field_biz__contains=biz).using("wechat").count()
        else:
            count = WechatAccountTask.objects.all().using("wechat").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class WechatAccountTaskDetailsView(View):
    """
        公众号任务详情
    """

    @staticmethod
    @login_level4_required
    def get(request, task_id):

        wat = WechatAccountTask.objects.filter(id=task_id).using("wechat").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wat)})

    @staticmethod
    @login_level4_required
    def post(request, task_id):
        params = json.loads(request.body)

        wat = WechatAccountTask.objects.filter(id=task_id).using("wechat").first()

        biz = check_gpc_undefined(params, "biz")
        is_zombie = check_gpc_undefined(params, "is_zombie", 0)

        if wat:
            wat.field_biz = biz
            wat.is_zombie = is_zombie
            wat.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Account Task not found"})


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
            warts = WechatArticle.objects.filter(title__contains=title).using("wechat").order_by("-publish_time").values()[::-1][(page - 1) * size:page * size]
        else:
            warts = WechatArticle.objects.all().using("wechat").values()[::-1][(page - 1) * size:page * size]
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
        pics_url = check_gpc_undefined(params, "pics_url")
        content_html = check_gpc_undefined(params, "content_html")
        source_url = check_gpc_undefined(params, "source_url")
        comment_id = check_gpc_undefined(params, "comment_id")
        sn = check_gpc_undefined(params, "sn")
        spider_time = check_gpc_undefined(params, "spider_time")

        wart = WechatArticle(field_biz=biz, account=account, title=title, url=url, author=author,
                             publish_time=publish_time, digest=digest, cover=cover, pics_url=pics_url,
                             content_html=content_html, source_url=source_url, comment_id=comment_id,
                             sn=sn, spider_time=spider_time)
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
            count = WechatArticle.objects.filter(title__contains=title).using("wechat").count()
        else:
            count = WechatArticle.objects.all().using("wechat").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class WechatArticleDetailsView(View):
    """
        公众号文章详情
    """

    @staticmethod
    @login_level4_required
    def get(request, art_id):

        wart = WechatArticle.objects.filter(id=art_id).using("wechat").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wart)})

    @staticmethod
    @login_level4_required
    def post(request, art_id):
        params = json.loads(request.body)

        wart = WechatArticle.objects.filter(id=art_id).using("wechat").first()

        account = check_gpc_undefined(params, "account")
        title = check_gpc_undefined(params, "title")
        url = check_gpc_undefined(params, "url")
        author = check_gpc_undefined(params, "author")
        publish_time = check_gpc_undefined(params, "publish_time")
        biz = check_gpc_undefined(params, "biz")
        digest = check_gpc_undefined(params, "digest")
        cover = check_gpc_undefined(params, "cover")
        pics_url = check_gpc_undefined(params, "pics_url")
        content_html = check_gpc_undefined(params, "content_html")
        source_url = check_gpc_undefined(params, "source_url")
        comment_id = check_gpc_undefined(params, "comment_id")
        sn = check_gpc_undefined(params, "sn")
        spider_time = check_gpc_undefined(params, "spider_time")

        if wart:
            wart.field_biz = biz
            wart.account = account
            wart.title = title
            wart.url = url
            wart.author = author
            wart.publish_time = publish_time
            wart.digest = digest
            wart.cover = cover
            wart.pics_url = pics_url
            wart.content_html = content_html
            wart.source_url = source_url
            wart.comment_id = comment_id
            wart.sn = sn
            wart.spider_time = spider_time
            wart.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Article Task not found"})


class WechatProfileListView(View):
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

        wps = WechatProfile.objects.all().using("wechat").values()[::-1][(page - 1) * size:page * size]

        return JsonResponse({"code": 200, "status": True, "message": list(wps)})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        profile_name = check_gpc_undefined(params, "profile_name")
        value = check_gpc_undefined(params, "value")

        wps = WechatProfile(profile_name=profile_name, value=value)
        wps.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class WechatProfileDetailsView(View):
    """
        爬虫配置详情
    """

    @staticmethod
    @login_level4_required
    def get(request, pro_id):

        wps = WechatProfile.objects.filter(id=pro_id).using("wechat").values()

        return JsonResponse({"code": 200, "status": True, "message": list(wps)})

    @staticmethod
    @login_level4_required
    def post(request, pro_id):
        params = json.loads(request.body)

        wp = WechatProfile.objects.filter(id=pro_id).using("wechat").first()

        profile_name = check_gpc_undefined(params, "profile_name")
        value = check_gpc_undefined(params, "value")

        if wp:
            wp.profile_name = profile_name
            wp.value = value
            wp.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "Wechat Profile not found"})
