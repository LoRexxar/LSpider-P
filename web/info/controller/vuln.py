#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: vuln.py
@time: 2023/6/7 19:10
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
from web.info.models import VulnData, VulnMonitorTask


class VulnMonitorTaskListView(View):
    """
        漏洞监控列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 10
        page = 1
        task_name = ""

        if "page" in request.GET:
            page = int(request.GET['page'])

        if "size" in request.GET:
            size = int(request.GET['size'])

        if "task_name" in request.GET:
            task_name = request.GET['task_name'].strip()

        if task_name:
            vmts = VulnMonitorTask.objects.filter(task_name__contains=task_name).using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        else:
            vmts = VulnMonitorTask.objects.all().using("lmonitor").values()[::-1][(page - 1) * size:page * size]
        count = len(vmts)

        return JsonResponse({"code": 200, "status": True, "message": list(vmts), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        task_name = check_gpc_undefined(params, "task_name")
        target = check_gpc_undefined(params, "target")
        is_active = check_gpc_undefined(params, "is_active", 1)

        vmt = VulnMonitorTask(task_name=task_name, target=target, is_active=is_active)
        vmt.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class VulnMonitorTaskCountView(View):
    """
        漏洞任务列表
    """

    @staticmethod
    @login_level4_required
    def get(request):
        task_name = ""

        if "task_name" in request.GET:
            task_name = request.GET['task_name']

        if type:
            count = VulnMonitorTask.objects.filter(task_name__contains=task_name).using("lmonitor").count()
        else:
            count = VulnMonitorTask.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class VulnMonitorTaskDetailsView(View):
    """
        漏洞任务详情
    """

    @staticmethod
    @login_level4_required
    def get(request, task_id):

        vmts = VulnMonitorTask.objects.filter(id=task_id).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(vmts)})

    @staticmethod
    @login_level4_required
    def post(request, task_id):
        params = json.loads(request.body)

        vmt = VulnMonitorTask.objects.filter(id=task_id).using("lmonitor").first()

        task_name = check_gpc_undefined(params, "task_name")
        target = check_gpc_undefined(params, "target")
        is_active = check_gpc_undefined(params, "is_active", 1)

        if vmt:
            vmt.task_name = task_name
            vmt.target = target
            vmt.is_active = is_active
            vmt.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "VulnMonitor Task not found"})


class VulnDataListView(View):
    """
        漏洞列表
    """

    @staticmethod
    @login_level2_required
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
            vds = VulnData.objects.filter(title__contains=title).using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        else:
            vds = VulnData.objects.all().using("lmonitor").order_by("publish_time").values()[::-1][(page - 1) * size:page * size]
        count = len(vds)

        for vd in vds:
            vd['description'] = ""
            vd['solutions'] = ""
            vd['reference'] = ""

            local_tz = pytz.timezone('Asia/Shanghai')
            vd['publish_time'] = vd['publish_time'].replace(tzinfo=local_tz).strftime("%Y-%m-%d %H:%M:%S")

        return JsonResponse({"code": 200, "status": True, "message": list(vds), "total": count})

    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        sid = check_gpc_undefined(params, "sid")
        cveid = check_gpc_undefined(params, "cveid")
        title = check_gpc_undefined(params, "title")
        vtype = check_gpc_undefined(params, "type")
        score = check_gpc_undefined(params, "score", 0)
        severity = check_gpc_undefined(params, "severity", 0)
        publish_time = check_gpc_undefined(params, "publish_time")
        description = check_gpc_undefined(params, "description")
        solutions = check_gpc_undefined(params, "solutions")
        link = check_gpc_undefined(params, "link")
        tag = check_gpc_undefined(params, "tag")
        source = check_gpc_undefined(params, "source")
        reference = check_gpc_undefined(params, "reference")
        is_poc = check_gpc_undefined(params, "is_poc", 1)
        is_exp = check_gpc_undefined(params, "is_exp", 1)
        is_verify = check_gpc_undefined(params, "is_verify", 1)
        is_active = check_gpc_undefined(params, "is_active", 1)
        state = check_gpc_undefined(params, "state", 0)

        vd = VulnData(sid=sid, cveid=cveid, title=title, type=vtype, score=score, severity=severity,
                      publish_time=publish_time, description=description, solutions=solutions, link=link,
                      tag=tag, source=source, reference=reference, state=state, is_poc=is_poc, is_exp=is_exp,
                      is_verify=is_verify, is_active=is_active)
        vd.save()
        return JsonResponse({"code": 200, "status": True, "message": "Insert success."})


class VulnDataCountView(View):
    """
        漏洞列表
    """

    @staticmethod
    @login_level2_required
    def get(request):
        title = ""

        if "title" in request.GET:
            title = request.GET['title']

        if type:
            count = VulnData.objects.filter(title__contains=title).using("lmonitor").count()
        else:
            count = VulnData.objects.all().using("lmonitor").count()
        return JsonResponse({"code": 200, "status": True, "total": count})


class VulnDataDetailsView(View):
    """
        漏洞详情
    """

    @staticmethod
    @login_level2_required
    def get(request, vid):

        vds = VulnData.objects.filter(id=vid).using("lmonitor").values()

        return JsonResponse({"code": 200, "status": True, "message": list(vds)})

    @staticmethod
    @login_level4_required
    def post(request, vid):
        params = json.loads(request.body)

        vd = VulnData.objects.filter(id=vid).using("lmonitor").first()

        sid = check_gpc_undefined(params, "sid")
        cveid = check_gpc_undefined(params, "cveid")
        title = check_gpc_undefined(params, "title")
        vtype = check_gpc_undefined(params, "type")
        score = check_gpc_undefined(params, "score", 0)
        severity = check_gpc_undefined(params, "severity", 0)
        publish_time = check_gpc_undefined(params, "publish_time")
        description = check_gpc_undefined(params, "description")
        solutions = check_gpc_undefined(params, "solutions")
        link = check_gpc_undefined(params, "link")
        tag = check_gpc_undefined(params, "tag")
        source = check_gpc_undefined(params, "source")
        reference = check_gpc_undefined(params, "reference")
        is_poc = check_gpc_undefined(params, "is_poc", 1)
        is_exp = check_gpc_undefined(params, "is_exp", 1)
        is_verify = check_gpc_undefined(params, "is_verify", 1)
        is_active = check_gpc_undefined(params, "is_active", 1)
        state = check_gpc_undefined(params, "state", 0)

        if vd:
            vd.sid = sid
            vd.cveid = cveid
            vd.title = title
            vd.type = vtype
            vd.score = score
            vd.severity = severity
            vd.publish_time = publish_time
            vd.description = description
            vd.solutions = solutions
            vd.link = link
            vd.tag = tag
            vd.source = source
            vd.reference = reference
            vd.is_poc = is_poc
            vd.is_exp = is_exp
            vd.is_verify = is_verify
            vd.is_active = is_active
            vd.state = state
            vd.save()

            return JsonResponse({"code": 200, "status": True, "message": "update successful"})
        else:
            return JsonResponse({"code": 404, "status": False, "message": "VulnData not found"})
