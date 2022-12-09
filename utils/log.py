# -*- coding: utf-8 -*-

"""
    log
    ~~~

    Implements color logger

    :author:    LoRexxar <LoRexxar@gmail.com>
    :homepage:  https://github.com/wufeifei/cobra
    :license:   MIT, see LICENSE for more details.
    :copyright: Copyright (c) 2017 Feei. All rights reserved
"""
import os
import logging
import colorlog
import time
import datetime
from web.index.models import BackendLog

# stream handle
#
# Copyright (C) 2010-2012 Vinay Sajip. All rights reserved. Licensed under the new BSD license.
#
logger = logging.getLogger('LSpider')
log_path = 'logs'


def log(loglevel, log_name):
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )
    )
    f = open(log_name, 'a+')
    handler2 = logging.StreamHandler(f)
    formatter = logging.Formatter(
        "[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s")
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    logger.addHandler(handler)
    logger.setLevel(loglevel)

    # hook info
    def newinfo(text):
        backendLog("system", text)
        logger.oldinfo(text)

    logger.oldinfo = logger.info
    logger.info = newinfo


def backendLog(log_type, log_text):
    """
    特殊日志进数据库
    :param log_type: 指的是log的类型比如system
    :param log_text:
    :return:
    """
    bl = BackendLog(type=log_type, log_text=log_text)
    bl.save()


if os.path.isdir(log_path) is not True:
    os.mkdir(log_path, 0o755)

day_time = int(time.mktime(datetime.date.today().timetuple()))
logfile = os.path.join(log_path, str(day_time)+'.log')

# log
log(logging.INFO, logfile)
