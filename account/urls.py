#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    # test
    # url(r'^$', 'account.views.first_page'),

    # 账户操作
    url(r'^add/$', 'user_add_view'),
    url(r'^add/action/$', 'user_add_action'),
    url(r'^list/$', 'user_list_view'),
    # url(r'^(\d*)/$', 'user_view_view'),

    #  登陆登出
    url(r'^login/$', "login_view"),
    url(r'^login/action/$', "login_action"),
    url(r'^logout/$', "logout_action"),
)