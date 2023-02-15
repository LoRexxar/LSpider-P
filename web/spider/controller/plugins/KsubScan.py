#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: KsubScan.py
@time: 2023/2/15 19:15
@desc:

'''

import requests
import traceback
import subprocess
from bs4 import BeautifulSoup

from utils.LReq import LReq
from utils.log import logger

from LSpider.settings import KSUBDOMAIN_PATH


class KsubScan:
    def __init__(self):
        self.req = LReq()
        self.kspath = KSUBDOMAIN_PATH
        logger.info("[Pre Scan][KsubScan] start Ksubdomain scan.")

    def query(self, domain, deep=0):

        try:
            p = subprocess.Popen(["sudo", self.kspath, "enum", "-d", domain, "--silent"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except:
            logger.warning("[Pre Scan][KsubScan] ksubdomain {} scan error.".format(domain))
            logger.warning("[Pre Scan][KsubScan] {}", p.stderr.read().decode())
            return False

        result = self.domainparse(domain, p.stdout.read().decode())
        print(result)
        result = []
        return result

    def domainparse(self, domain, result):
        result_list = []

        try:
            for target in result:
                t = target.split("=>")
                subdomain = t[0]
                ip = t[-1]
                print(subdomain)
                print(ip)
                result_list.append(subdomain.strip())

        except:
            traceback.print_exc()
            logger.warning("[Pre Scan][CrtScan] {} parse error.".format(domain))
            return False

        return result_list


if __name__ == "__main__":
    Req = KsubScan()

    Req.query("seebug.org")
