#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: KsubScan.py
@time: 2023/2/15 19:15
@desc:

'''

import os
import re
import traceback
import subprocess

from utils.LReq import LReq
from utils.log import logger

from LSpider.settings import KSUBDOMAIN_PATH
from web.spider.models import SubIpList


class KsubScan:
    def __init__(self):
        self.req = LReq()
        self.kspath = KSUBDOMAIN_PATH
        self.is_install = True

        if not os.path.exists(self.kspath):
            self.is_install = False
            logger.warning("[Pre Scan][KsubScan] Ksubdomain path {} not found. need install.".format(self.kspath))

        logger.info("[Pre Scan][KsubScan] start Ksubdomain scan.")

    def query(self, domain, deep=0):
        try:
            if not self.is_install:
                return []

            p = subprocess.Popen(["sudo", self.kspath, "enum", "-d", domain, "--silent"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except:
            logger.warning("[Pre Scan][KsubScan] ksubdomain {} scan error.".format(domain))
            logger.warning("[Pre Scan][KsubScan] {}", p.stderr.read().decode())
            return False

        result = self.domain_parse(domain, p.stdout.read().decode())
        return result

    def check_ip_exist(self, domain, ip):
        # 检查ip的格式
        matchobj = re.match(ip, "[0-9]{1,3}(\.[0-9]{1,3}){1,3}", re.M | re.I)
        if not matchobj:
            return False

        si = SubIpList.objects.filter(subdomain=domain)
        if not si:
            si = SubIpList(subdomain=domain, ips=ip)
            si.save()
        else:
            si.ips = ip
            si.save()

        return True

    def domain_parse(self, domain, result):
        result_list = []

        try:
            for target in result.split("\n"):
                t = target.split("=>")
                subdomain = t[0].strip()
                ip = t[-1].strip()
                self.check_ip_exist(subdomain, ip)

                if subdomain:
                    result_list.append(subdomain.strip())

        except:
            traceback.print_exc()
            logger.warning("[Pre Scan][CrtScan] {} parse error.".format(domain))
            return False

        return result_list


if __name__ == "__main__":
    Req = KsubScan()

    Req.query("seebug.org")
