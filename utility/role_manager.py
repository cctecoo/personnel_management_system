#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'
from django.contrib.auth.models import Group


ROLE_STAFF = 10
ROLE_HR = 20
ROLE_MANAGER = 50
ROLE_SYSADMIN = 99
ROLES = {
    ROLE_STAFF: u'员工',
    ROLE_HR: u'人事',
    ROLE_MANAGER: u'经理',
    ROLE_SYSADMIN: u'系统管理员',
}


# 根据角色组别的id获得文字描述s
def get_role(role):
    if role not in ROLES:
        return None

    return Group.objects.get_or_create(name=ROLES[role])[0]


# 根据文字描述获得角色组别的id
def get_role_id(name):
    for k, v in ROLES.items():
        if v == name:
            return k
    return None


# 检查当前用户是否符合给定组别
def check_role(request, role):
    if role == ROLE_SYSADMIN and request.user.is_superuser:
        return True

    user = request.user
    return ROLES.has_key(role) and user.groups.filter(name=ROLES[role]).exists()
