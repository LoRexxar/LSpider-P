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

        result = p.stdout.read().decode()
        print(result)
        result = []
        return result

    def domainparse(self, domain, content):
        result_list = [domain]

        try:
            soup = BeautifulSoup(content, "html.parser")

            tr_tag_list = soup.find_all('tr')

            for tr_tag in tr_tag_list:
                td_tag = tr_tag.find_all('td')

                if len(td_tag) > 4:
                    predomain_list = td_tag[4].contents

                    for predoamin in predomain_list:
                        if '.' in predoamin and '*' not in predoamin:
                            if predoamin not in result_list:
                                result_list.append(predoamin.strip())

        except:
            traceback.print_exc()
            logger.warning("[Pre Scan][CrtScan] {} parse error.".format(domain))
            return False

        return result_list


if __name__ == "__main__":
    Req = KsubScan()

    Req.query("seebug.org")
