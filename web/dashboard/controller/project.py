#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: project.py
@time: 2023/7/20 17:56
@desc:

'''


from web.dashboard.models import Project, ProjectSource, ProjectAssets, ProjectIps, ProjectVuls, ProjectSubdomain, ProjectAnnouncement
from web.info.models import RssArticle, RssMonitorTask, WechatArticle, WechatAccountTask


def check_project_wechat_update():
    """
    检查project对应的公众号更新同步
    :return:
    """
    pss = ProjectSource.objects.filter(type=2)
    for ps in pss:
        wechat_name = ps.content
        rmt = RssMonitorTask.objects.filter(name=wechat_name).first()

        if rmt:
            ras = RssArticle.objects.filter(rss_id=rmt.id)

            for ra in ras:
                # 读取project source中的所有公众号对应的文章
                title = ra.title
                link = ra.url
                author = ra.author
                content = ra.content_html
                create_time = ra.publish_time

                pa = ProjectAnnouncement.objects.filter(title=title, project_id=ps.id).first()
                if not pa:
                    pa2 = ProjectAnnouncement(project_id=ps.id, title=title, author=author,
                                              content=content, create_time=create_time, is_active=1, link=link,
                                              )
                    pa2.save()
    return
