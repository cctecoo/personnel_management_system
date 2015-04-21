#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('information.views',
    # 个人信息
    url(r'^personal/(\d*)/$', 'information_personal_view'),
    url(r'^personal/(\d*)/edit/action/$', 'information_personal_edit_action'),

    # 工作经历 start
    url(r'^personal/(\d+)/job/list/$', 'job_list_view'),  # 工作一览view
    url(r'^personal/(\d+)/job/edit/(\d+)/$', 'job_edit_view'),  # 工作编辑view
    url(r'^personal/(\d+)/job/edit/action/$', 'job_edit_action'),  # 工作编辑action
    url(r'^personal/(\d+)/job/add/$', 'job_add_view'),  # 工作添加view
    url(r'^personal/(\d+)/job/delete/action/$', 'job_delete_action'),  # 工作删除action
    # 工作经历 end

    # 教育经历 start
    url(r'^personal/(\d+)/education/list/$', 'education_list_view'),  # 教育一览view
    url(r'^personal/(\d+)/education/edit/(\d+)/$', 'education_edit_view'),  # 教育经历编辑view
    url(r'^personal/(\d+)/education/edit/action/$', 'education_edit_action'),  # 教育经历编辑action
    url(r'^personal/(\d+)/education/add/$', 'education_add_view'),  # 教育经历添加view
    url(r'^personal/(\d+)/education/delete/action/$', 'education_delete_action'),  # 教育经历删除action
    # 教育经历 end

    # url(r'^contacts/$', 'information_contacts_view'),

    )

