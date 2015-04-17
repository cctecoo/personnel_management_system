#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('information.views',
    # start
    url(r'^personal/(\d*)/$', 'information_personal_view'),
    url(r'^personal/(\d*)/edit/action/$', 'information_personal_edit_action'),

    # url(r'^contacts/$', 'information_contacts_view'),

    )

