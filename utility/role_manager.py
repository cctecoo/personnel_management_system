#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cc'
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from account.models import User

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
    return ROLES. has_key(role) and user.groups.filter(name=ROLES[role]).exists()


# 检查当前用户是否符合操作权限级别
# 既只能对自己或者低于自己权限用户进行操作
def check_permission_allowed(request, id):
    user = get_object_or_404(User, id=id)
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    role_id = get_role_id(role_name) if role_name else None

    if check_role(request, ROLE_MANAGER) and ((role_id == ROLE_MANAGER and request.user.id != long(id))
                                              or user.is_superuser):
        return False
    if check_role(request, ROLE_HR) and ((role_id == ROLE_HR and request.user.id != long(id))
                                         or role_id not in (ROLE_STAFF, ROLE_HR)):
        return False
    if check_role(request, ROLE_STAFF) and user.username != request.user.username:
        return False
    return True