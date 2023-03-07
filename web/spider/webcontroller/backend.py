#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: backend.py
@time: 2023/2/23 17:35
@desc:

'''

from __future__ import unicode_literals

import os
import json
import time
import codecs

from django.views import View
from django.http import HttpResponse, JsonResponse

from web.dashboard.models import ProjectSubdomain, Project
from web.spider.models import SubDomainList, SubIpList
from web.index.middleware import login_level1_required, login_level2_required, login_level3_required, login_level4_required, login_required
from utils.base import check_gpc_undefined


class SubdomainGroupListView(View):
    """
        未分配域名聚合结果
    """

    @staticmethod
    @login_level4_required
    def get(request):
        size = 1
        result_list = []

        if "size" in request.GET:
            size = int(request.GET['size'])

        # 获取一个没有被分配的域名
        subs = SubDomainList.objects.filter(is_assign=False)[:size]

        if not subs:
            return JsonResponse({"code": 404, "status": False, "message": "Not Found unassign Subdomain."})

        for sub in subs:
            subdomain = sub.subdomain
            subdomain_parse = subdomain.split(".")[-2:]
            root_domain = ".".join(subdomain_parse)

            # 特殊后缀特殊处理
            if root_domain.lower() in ["com.cn", "com.hk", "com.ar", "com.au"]:
                subdomain_parse = subdomain.split(".")[-3:]

            root_domain = ".".join(subdomain_parse)
            subdomain_list = []

            # 根据根域名来聚合其他未分配的域名
            subds = SubDomainList.objects.filter(subdomain__iendswith=root_domain, is_assign=False)
            for subd in subds:
                subdomain_list.append(subd.subdomain)

            result = {
                "root": root_domain,
                "subdomain_list": subdomain_list,
            }
            result_list.append(result)

        sub_count = len(result_list)

        return JsonResponse({"code": 200, "status": True, "message": result_list, "total": sub_count})


class SubdomainGroupAssignView(View):
    """
        分配聚合后的域名结果
    """
    @staticmethod
    @login_level4_required
    def post(request):
        params = json.loads(request.body)

        project_id = check_gpc_undefined(params, "project_id", 0)
        root_domain = check_gpc_undefined(params, "rootdomain")

        p = Project.objects.filter(id=project_id).first()
        if not p:
            return JsonResponse({"code": 404, "status": False, "message": "Not Found Project {}.".format(p.id)})

        if not root_domain:
            return JsonResponse({"code": 404, "status": False, "message": "missing required parameter"})

        # 根据根域名来聚合其他未分配的域名
        subds = SubDomainList.objects.filter(subdomain__iendswith=root_domain, is_assign=False)

        # 分配根域名给project
        psub = ProjectSubdomain(project_id=p.id, subdomain=root_domain, weight=0, is_active=1)
        psub.save()

        for subd in subds:
            psub = ProjectSubdomain.objects.filter(project_id=p.id, subdomain=subd.subdomain).first()
            if not psub:
                # 分配给project
                psub = ProjectSubdomain(project_id=p.id, subdomain=subd.subdomain, title=subd.title, banner=subd.banner,
                                        weight=1, is_active=1)
                psub.save()

            # 修改is_assign
            subd.is_assign = True
            subd.save()

        return JsonResponse({"code": 200, "status": True, "message": "Project root domain assign successful"})
