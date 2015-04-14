#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'


class PermissionDeniedError(Exception):
    """
    没有权限访问
    """
    def __init__(self):
        super(PermissionDeniedError, self).__init__(u"您没有权限访问本页面。")
