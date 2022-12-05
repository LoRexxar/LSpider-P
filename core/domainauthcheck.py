#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: domainauthcheck.py.py
@time: 2020/9/28 18:15
@desc:

'''


from urllib.parse import urlparse, parse_qs, urljoin

from web.index.models import AccountDataTable, LoginPageList

from utils.log import logger, backendLog
from utils.wechathandler import ReMess


def check_login_or_get_cookie(url, title=""):
    """
    检查页面权限并返回cookie
    :param title:
    :param url:
    :return:
    """
    domain = urlparse(url).netloc

    ad = AccountDataTable.objects.filter(domain=domain).first()

    if ad:
        logger.debug("[Check Login] Url {} get login cookie.".format(url))
        back_cookie = ad.cookies

        return back_cookie, True

    else:
        # 检查上层域名是否存在鉴权保存数据
        parent_domain = ".".join(domain.split('.')[1:])

        pad = AccountDataTable.objects.filter(domain=parent_domain).first()

        if pad:
            logger.debug("[Check Login] Url {} use parent domain {} login cookie.".format(url, parent_domain))
            back_cookie = pad.cookies

            # 即便使用了上级域名的鉴权也需要记录
            lp = LoginPageList.objects.filter(domain=domain, is_active=True).first()

            if not lp:
                ReMess.debug_message("""New Login Page:
Domain: {}
Url: {}
Title: {}
""".format(domain, url, title))
                backendLog("newloginpage", "Url: {},Title: {}".format(url, title))

                nlp = LoginPageList(domain=domain, url=url, title=title)
                nlp.save()

            return back_cookie, False

        else:
            # 剩余的都要保留并推送
            # 即便使用了上级域名的鉴权也需要记录
            lp = LoginPageList.objects.filter(domain=domain, is_active=True).first()

            if not lp:
                ReMess.debug_message("""New Login Page:
Domain: {}
Url: {}
Title: {}
""".format(domain, url, title))
                backendLog("newloginpage", "Url: {},Title: {}".format(url, title))

                nlp = LoginPageList(domain=domain, url=url, title=title)
                nlp.save()

            return "", False
