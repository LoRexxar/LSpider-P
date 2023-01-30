#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: spider.py
@time: 2020/3/12 15:54
@desc:
'''

import time
import datetime
import traceback
import threading
import json
from pika import exceptions as pika_exceptions
from queue import Queue, Empty
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from utils.LReq import LReq
from utils.log import logger, backendLog
from utils.base import get_new_scan_id, get_now_scan_id
from utils.base import check_target

from core.htmlparser import html_parser
from core.urlparser import url_parser, checkbanlist
from core.threadingpool import ThreadPool
from core.rabbitmqhandler import RabbitmqHandler
from core.domainauthcheck import check_login_or_get_cookie

from LSpider.settings import LIMIT_DEEP, IS_OPEN_RABBITMQ
from LSpider.settings import IS_OPEN_CHROME_PROXY, CHROME_PROXY

from web.spider.models import UrlTable, SubDomainList
from web.index.models import ScanTask

from web.spider.controller.prescan import PrescanCore


class SpiderCoreBackend:
    """
    spider 守护线程
    """
    def __init__(self):
        # 任务与线程分发
        self.target_list = Queue()
        self.emergency_target_list = Queue()
        self.threadpool = ThreadPool()
        self.scan_id = get_now_scan_id()

        self.check_task()
        # 获取线程池然后分发信息对象
        # 当有空闲线程时才继续
        i = 0

        # 启动1个线程用于紧急任务
        while i < 1:
            i += 1
            spidercore = SpiderCore(self.emergency_target_list)

            logger.debug("[Spider Core] New Thread {} for emergency Spider Core.".format(i))

            if IS_OPEN_RABBITMQ:
                self.threadpool.new(spidercore.scancore, args=(True,))
            else:
                self.threadpool.new(spidercore.scan_for_queue)
            time.sleep(0.5)

        while 1:
            while self.threadpool.get_free_num():

                if i > 100:
                    logger.warning("[Spider Core] More than 100 thread init. stop new Thread.")
                    self.threadpool.wait_all_thread()
                    break

                else:

                    i += 1
                    spidercore = SpiderCore(self.target_list)

                    logger.debug("[Spider Core] New Thread {} for Spider Core.".format(i))

                    if IS_OPEN_RABBITMQ:
                        self.threadpool.new(spidercore.scancore)
                    else:
                        self.threadpool.new(spidercore.scan_for_queue)

                    time.sleep(3)

            # self.threadpool.wait_all_thread()
            # 60s 检查一次任务以及线程状态
            self.check_task()
            time.sleep(600)

    def check_task(self):

        # rabbitmq init
        if IS_OPEN_RABBITMQ:
            self.rabbitmq_handler = RabbitmqHandler()

        # 如果有任务跑在rabbitmq上那么现在不新建任务

        if IS_OPEN_RABBITMQ:
            left_tasks = self.rabbitmq_handler.get_scan_ready_count()
            left_emergency_tasks = self.rabbitmq_handler.get_emergency_scan_ready_count()
        else:
            left_tasks = self.target_list.qsize()
            left_emergency_tasks = self.emergency_target_list.qsize()

        logger.info("[Spider Main] now {} targets left.".format(left_tasks))
        logger.info("[Spider Main] Emergency Task left {} targets.".format(left_emergency_tasks))

        if left_tasks > 100:
            logger.debug("[Spider Main] Left Tasks more than 100. pause to start new task.")
            return

        # checkstatus
        tasklist = ScanTask.objects.filter(is_active=True, is_finished=False)

        if tasklist:
            # 获得新任务的scan_id
            self.scan_id = get_new_scan_id()

            t = threading.Thread(target=self.init_scan)
            t.start()
            time.sleep(3)

        # 如果队列为空，那么直接跳出
        if IS_OPEN_RABBITMQ:
            if not self.rabbitmq_handler.get_scan_ready_count():
                logger.debug("[Spider Core] Spider Target Queue is empty.")
                return

        if not IS_OPEN_RABBITMQ and self.target_list.empty():
            logger.debug("[Spider Core] Spider Target Queue is empty.")
            return

        logger.info("[Spider Main] Spider id {} Start...".format(self.scan_id))

    def init_scan(self):

        tasklist = ScanTask.objects.filter(is_active=True, is_finished=False)
        new_task = False
        target_cookies = ""
        task_is_emergency = False

        # 提取出未启动的任务
        for task in tasklist:
            lastscantime = datetime.datetime.strptime(str(task.last_scan_time)[:19], "%Y-%m-%d %H:%M:%S")
            nowtime = datetime.datetime.now()

            # if lastscantime:
                # if (nowtime - lastscantime).days > 90:
                # 3 mouth
                # 暂时改为单次扫描，每个任务标记并只扫描一次

            targets = check_target(task.target)
            target_type = task.target_type
            target_cookies = task.cookies
            task_is_emergency = task.is_emergency

            # 标志任务开始
            backendLog("info", "New Task {} start to scan.New Scan id {}".format(task.task_name, self.scan_id))
            task.last_scan_time = nowtime
            task.last_scan_id = self.scan_id
            task.is_emergency = False
            task.is_finished = True
            task.save()

            for target in targets:

                if IS_OPEN_RABBITMQ:
                    if task_is_emergency:
                        self.rabbitmq_handler.new_emergency_scan_target(
                            json.dumps({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0}))
                    else:
                        self.rabbitmq_handler.new_scan_target(json.dumps({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0}), weight=1)
                else:
                    self.target_list.put({'url': target, 'type': target_type, 'cookies': target_cookies, 'deep': 0})

                # subdomain scan
                domain = urlparse(target).netloc

                if domain:
                    PrescanCore().start(domain, is_emergency=task.is_emergency)

            # 每次只读一个任务，在一个任务后退出重启
            # 紧急任务不影响到普通任务
            if task_is_emergency:
                new_task = False
            else:
                new_task = True

            if new_task:
                # 每次只读一个任务，在一个任务后退出重启
                break

        logger.debug("[INIT Scan] Target init success.")

        subdomainlist = SubDomainList.objects.filter(is_finished=False)

        for subdomain in subdomainlist:
            lastscantime = datetime.datetime.strptime(str(subdomain.lastscan)[:19], "%Y-%m-%d %H:%M:%S")
            nowtime = datetime.datetime.now()

            if lastscantime:
                # if (nowtime - lastscantime).days > 30:
                # 1 mouth
                target = subdomain.subdomain.strip()

                if IS_OPEN_RABBITMQ:
                    if subdomain.is_emergency:
                        self.rabbitmq_handler.new_emergency_scan_target(json.dumps(
                            {'url': "http://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))
                        self.rabbitmq_handler.new_emergency_scan_target(json.dumps(
                            {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}))

                    else:
                        self.rabbitmq_handler.new_scan_target(json.dumps({'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}), weight=1)
                        self.rabbitmq_handler.new_scan_target(json.dumps(
                            {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0}), weight=1)
                else:
                    self.target_list.put(
                        {'url': "http://"+target, 'type': 'link', 'cookies': target_cookies, 'deep': 0})
                    self.target_list.put(
                        {'url': "https://" + target, 'type': 'link', 'cookies': target_cookies, 'deep': 0})

                # 重设扫描时间
                subdomain.lastscan = nowtime
                subdomain.is_finished = True
                subdomain.save()


class SpiderCore:
    """
    spider core thread
    """

    def __init__(self, target=Queue()):

        # rabbitmq init
        if IS_OPEN_RABBITMQ:
            self.rabbitmq_handler = RabbitmqHandler()

        # self.target = target
        self.target_list = target

        self.req = LReq(is_chrome=True)
        self.scan_id = get_now_scan_id()
        self.i = 1

    def scancore(self, is_emergency=False):
        # start
        if is_emergency:
            logger.info("[Scan Core] Emergency Scan Task start:>")
            self.rabbitmq_handler.start_emergency_scan_target(self.scan_emergency_task_distribute)
        else:
            logger.info("[Scan Core] Scan Task start:>")
            self.rabbitmq_handler.start_scan_target(self.scan_task_distribute)

    def scan_task_distribute(self, channel, method, header, message):

        # 确认收到消息
        channel.basic_ack(delivery_tag=method.delivery_tag)

        try:
            # 获取任务权重
            task_weight = int(header.priority)

            # 获取任务信息
            task = json.loads(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task, task_weight=task_weight)
        except json.decoder.JSONDecodeError:
            # 获取任务权重
            task_weight = int(header.priority)
            task = eval(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return False

            self.scan(task, task_weight=task_weight)

        except:
            # 任务启动错误则把任务重新插回去
            self.rabbitmq_handler.new_scan_target(message, weight=1)
            time.sleep(0.5)
            return False

    def scan_emergency_task_distribute(self, channel, method, header, message):

        # 确认收到消息
        channel.basic_ack(delivery_tag=method.delivery_tag)

        try:

            # 获取任务信息
            task = json.loads(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return True

            if task['deep'] == 0:
                backend_cookies, auth_status = check_login_or_get_cookie(task['url'])

                if not backend_cookies:
                    # 如果为空，那么还没设置好鉴权
                    logger.debug("[INIT][DISTRIBUTE] url {} back rabbitmq".format(message))
                    self.rabbitmq_handler.new_emergency_scan_target(message)
                    time.sleep(0.5)
                    return False

                else:
                    # 将设置好鉴权的任务放回主线程
                    # 如果使用了父节点的cookie，那么紧急队列挂起
                    task['cookie'] = backend_cookies
                    message = json.dumps(task)

                    logger.debug("[INIT][DISTRIBUTE] url {} back to main Thread".format(message))
                    self.rabbitmq_handler.new_scan_target(message, weight=5)
                    if not auth_status:
                        self.rabbitmq_handler.new_emergency_scan_target(message)

                    time.sleep(0.5)
                    return True

            else:
                # 将设置好鉴权的任务和不满足条件的都放回主线程
                logger.debug("[INIT][DISTRIBUTE] url {} back to main Thread".format(message))
                self.rabbitmq_handler.new_scan_target(message, weight=5)
                time.sleep(0.5)
                return True

            # self.scan(task, is_emergency=True)
        except json.decoder.JSONDecodeError:
            task = eval(message)

            if checkbanlist(task['url']):
                logger.debug(("[Scan] ban domain exist...continue"))
                return True

            if task['deep'] == 0:
                backend_cookies, auth_status = check_login_or_get_cookie(task['url'])

                if not backend_cookies:
                    # 如果为空，那么还没设置好鉴权
                    logger.debug("[INIT][DISTRIBUTE] json url {} back rabbitmq".format(message))
                    self.rabbitmq_handler.new_emergency_scan_target(message)
                    time.sleep(0.5)
                    return True

                else:
                    # 将设置好鉴权的任务放回主线程
                    task['cookie'] = backend_cookies
                    message = json.dumps(task)

                    logger.debug("[INIT][DISTRIBUTE] url {} back to main Thread".format(message))
                    self.rabbitmq_handler.new_scan_target(message, weight=5)

                    if not auth_status:
                        self.rabbitmq_handler.new_emergency_scan_target(message)

                    time.sleep(0.5)
                    return True

            else:
                # 将设置好鉴权的任务和不满足条件的都放回主线程
                logger.debug("[INIT][DISTRIBUTE] url {} back to main Thread".format(message))
                self.rabbitmq_handler.new_scan_target(message, weight=5)
                time.sleep(0.5)
                return True

            # self.scan(task, is_emergency=True)

        except:
            # 任务启动错误则把任务重新插回去
            logger.debug("[INIT] Something error...{}".format(traceback.format_exc()))
            self.rabbitmq_handler.new_emergency_scan_target(message)
            time.sleep(0.5)
            return False

    def scan_for_queue(self):

        i = 0

        while not self.target_list.empty() or i < 30:
            try:
                target = self.target_list.get(False)

                if checkbanlist(target['url']):
                    logger.debug(("[Scan] ban domain exist...continue"))
                    continue

                self.scan(target)

            except KeyboardInterrupt:
                logger.error("[Scan] Stop Scaning.")
                self.req.close_driver()
                exit(0)

            except Empty:
                i += 1
                time.sleep(1)

            except:
                logger.warning('[Scan] something error, {}'.format(traceback.format_exc()))
                raise

    def scan(self, target, is_emergency=False, task_weight=0):
        i = 0

        try:
            # sleep
            time.sleep(self.req.get_timeout())

            # target = self.target_list.get(False)
            code = -1
            content = False
            backend_cookies = ""
            title = ""

            # 发起对目标的请求
            if target['type'] == 'link':
                code, content, title = self.req.get(target['url'], 'RespByChrome', 0, target['cookies'])

            if target['type'] == 'js':
                code, content, title = self.req.get(target['url'], 'Resp', 0, target['cookies'])

            if code == -1:
                return

            # 如果这个页面需要登录，那么把链接塞入加急队列之后等待对应的鉴权被设置
            if code == 2:
                # 代表这个页面需要登录
                backend_cookies, auth_status = check_login_or_get_cookie(target['url'], title)

                # 任务塞到加急队列中
                new_target = target
                new_target['cookies'] = backend_cookies

                # 如果获取到鉴权，那么任务放回主线程并增加权重
                if backend_cookies:
                    self.rabbitmq_handler.new_scan_target(json.dumps(new_target), weight=5)
                else:
                    self.rabbitmq_handler.new_emergency_scan_target(json.dumps(new_target))

            else:
                backend_cookies = target['cookies']

            # 如果为deep=0
            # 那么记录title
            if target['deep'] == 0:
                domain = urlparse(target['url']).netloc

                sd = SubDomainList.objects.filter(subdomain=domain).first()

                if sd:
                    sd.title = title
                    sd.save()

            # 分割html页面
            result_list = html_parser(content)

            # 解析html中的url
            result_list = url_parser(target['url'], result_list, target['deep'], backend_cookies)

            # 继续把链接加入列表
            for target in result_list:

                if target['deep'] > LIMIT_DEEP:
                    continue

                # save to rabbitmq
                if IS_OPEN_RABBITMQ:
                    self.rabbitmq_handler.new_scan_target(json.dumps(target), weight=task_weight+1)
                else:
                    self.target_list.put(target)

                # self.target_list.put(target)

        except KeyboardInterrupt:
            logger.error("[Scan] Stop Scaning.")
            self.req.close_driver()
            exit(0)

        except Empty:
            i += 1
            time.sleep(1)

        except:
            logger.warning('[Scan] something error, {}'.format(traceback.format_exc()))
            raise

