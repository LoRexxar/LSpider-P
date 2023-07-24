#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: __init__.py.py
@time: 2023/7/20 17:54
@desc:

'''

import time
from utils.log import logger

from project import check_project_wechat_update


def traverse_task_list():
    task_list = [
        {
            "function": check_project_wechat_update,
            "time": 600,
        }
    ]

    logger.info("[init check] LSpider Data check before init.")
    for task in task_list:
        if time.time() % task['time'] < 10:
            task['function']()

    return True
