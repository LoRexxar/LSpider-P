#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: __init__.py.py
@time: 2020/3/11 16:22
@desc:
'''

from web.index.models import ConfigData
from utils.log import logger

DEFAULT_CONFIG_EXT = {
    "NOW_SPIDER_TASKID": "当前爬虫任务id",
    "LEFT_SPIDER_COUNT": "剩余爬虫任务数",
    "EMERGENCY_LEFT_SPIDER_COUNT": "剩余紧急爬虫任务数",
}


def init_config():
    for key in DEFAULT_CONFIG_EXT:
        cd = ConfigData.objects.filter(config_name=key).first()

        if not cd:
            c = ConfigData(config_name=key, ext=DEFAULT_CONFIG_EXT[key])
            c.save()

    logger.info("[SPIDER INIT] Spider config init success...")


def set_conig(name, data):
    if name not in DEFAULT_CONFIG_EXT:
        return False

    cd = ConfigData.objects.filter(config_name=name).first()

    if not cd:
        c = ConfigData(config_name=name, config_data=data, ext=DEFAULT_CONFIG_EXT[name])
        c.save()
        return True

    cd.config_data = data
    cd.save()
    return True
