#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('notice.views',
    # 公告信息

    url(r'^add/$', 'notice_add_view'),
    url(r'^add/action/$', 'notice_add_action'),
    # url(r'^delete/action/$', 'notice_delete_action'),
    url(r'^edit/(\d*)/$', 'notice_edit_view'),
    # url(r'^edit/action/$', 'notice_edit_action'),
    url(r'^list/$', 'notice_list_view'),
    # url(r'^(\d*)/$', 'notice_view_view'),

    )