#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: project.py
@time: 2023/7/20 17:56
@desc:

'''

from utils.log import logger

from web.dashboard.models import Project, ProjectSource, ProjectAssets, ProjectIps, ProjectVuls, ProjectSubdomain, ProjectAnnouncement
from web.info.models import RssArticle, RssMonitorTask, WechatArticle, WechatAccountTask


def check_project_wechat_update():
    """
    检查project对应的公众号更新同步
    :return:
    """
    logger.info("[init check] LSpider Data check before init.")
    pss = ProjectSource.objects.filter(type=2)

    for ps in pss:
        wechat_name = ps.content

        # rss check
        rmt = RssMonitorTask.objects.filter(name=wechat_name).using("lmonitor").first()

        if rmt:
            ras = RssArticle.objects.filter(rss_id=rmt.id).using("lmonitor")

            for ra in ras:
                # 读取project source中的所有公众号对应的文章
                title = ra.title
                link = ra.url
                author = ra.author
                content = ra.content_html
                create_time = ra.publish_time

                pa = ProjectAnnouncement.objects.filter(title=title, project_id=ps.project_id).first()
                if not pa:
                    pa2 = ProjectAnnouncement(project_id=ps.project_id, title=title, author=author,
                                              content=content, create_time=create_time, is_active=1, link=link,
                                              )
                    pa2.save()

        # wechat check
        wat = WechatAccountTask.objects.filter(account=wechat_name).using("lmonitor").first()

        if wat:
            was = WechatArticle.objects.filter(account=wechat_name).using("lmonitor")

            for wa in was:
                title = wa.title
                link = wa.url
                author = wa.account
                content = wa.content_html
                create_time = wa.publish_time

                pa = ProjectAnnouncement.objects.filter(title=title, project_id=ps.project_id).first()
                if not pa:
                    pa2 = ProjectAnnouncement(project_id=ps.project_id, title=title, author=author,
                                              content=content, create_time=create_time, is_active=1, link=link,
                                              )
                    pa2.create_time = create_time
                    pa2.save()
    return
