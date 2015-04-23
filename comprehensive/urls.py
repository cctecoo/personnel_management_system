#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('comprehensive.views',
    # 部门管理
    url(r'^department/list/$', 'department_list_view'),  # 部门一览view
    url(r'^department/add/$', 'department_add_view'),  # 部门增加view
    url(r'^department/add/action/$', 'department_add_action'),  # 部门增加action
    url(r'^department/edit/(\d*)/$', 'department_edit_view'),  # 部门修改view
    url(r'^department/edit/action/$', 'department_edit_action'),  # 部门修改action
    url(r'^department/delete/action/$', 'department_delete_action'),  # 部门删除action

    # url(r'^department/set/$', 'department_set_view'),  # 人员部门配置view

    )