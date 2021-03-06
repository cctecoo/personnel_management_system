#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'personnel_management_system.views.home', name='home'),
    # url(r'^personnel_management_system/', include('personnel_management_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # 默认主页
    url(r'^$', "personnel_management_system.views.index_view"),

    # 账户管理模块
    url(r'^account/', include('account.urls')),

    # 基础信息模块
    url(r'^information/', include('information.urls')),

    # 综合管理模块
    url(r'^comprehensive/', include('comprehensive.urls')),

    # 公告模块
    url(r'^notice/', include('notice.urls')),
)
