#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    # test
    # url(r'^$', 'account.views.first_page'),

    # 账户操作

    #  登陆待完成
    url(r'^login/$', "login_view"),
    url(r'^login/action/$', "login_action"),
    url(r'^logout/$', "logout_action"),
)