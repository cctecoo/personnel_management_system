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

    url(r'^department/set/$', 'department_set_view'),  # 人员部门配置view
    url(r'^department/set/edit/action/$', 'department_set_edit_action'),  # 人员部门配置action

    url(r'^status/set/edit/action/$', 'status_set_edit_action'),  # 人员状态配置action

    # 签到
    url(r'^check_in/(\d*)/$', 'check_in_personal_view'),  # 个人考勤view
    url(r'^check_in/(\d*)/list/$', 'check_in_personal_list_view'),  # 个人考勤list view
    url(r'^check_in/all/list/$', 'check_in_all_list_view'),  # 所有人考勤记录view
    url(r'^check_in/action/$', 'check_in_action'),  # 签到action

    )