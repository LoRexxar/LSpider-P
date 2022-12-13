# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class ScanTask(models.Model):
    task_name = models.CharField(max_length=50)
    target = models.TextField()
    target_type = models.CharField(max_length=30, default='link')
    task_tag = models.CharField(max_length=100)
    last_scan_time = models.DateTimeField(auto_now=True)
    last_scan_id = models.IntegerField(default=0)
    cookies = models.CharField(max_length=5000, default=None, null=True)
    is_active = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)


class BanList(models.Model):
    ban_name = models.CharField(max_length=50)
    ban_domain = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)


class AccountDataTable(models.Model):
    domain = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    iphone = models.CharField(max_length=50, null=True)
    cookies = models.TextField(null=True)


class LoginPageList(models.Model):
    domain = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=200, default="", null=True)
    is_active = models.BooleanField(default=True)


class BackendLog(models.Model):
    type = models.CharField(max_length=30)
    log_text = models.TextField(null=True)
    log_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)


class FrontLog(models.Model):
    user_id = models.IntegerField()
    type = models.CharField(max_length=30)
    log_text = models.TextField(null=True)
    log_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
