#!/usr/bin/env python
# -*- coding: utf-8 -*-
from account.models import User

__author__ = 'cc'
from datetime import date, datetime

from django import template
from django.db import connection
from django.template.defaultfilters import register
from django.utils.encoding import force_unicode
from django.conf import settings

from comprehensive.models import Department


register = template.Library()


@register.filter(name='in_group')
def in_group(user, groups):
    """Returns a boolean if the epiao_account is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if account|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if account|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    group_list = force_unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))


@register.filter(name='get_sex_name')
def get_sex_name(value):
    """取得性别中文"""
    if value == 1:
        return u"男"
    else:
        return u"女"


@register.filter(name='get_personal_status')
def get_personal_status(value):
    """取得员工状态"""
    if value == 0:
        return u"实习"
    elif value == 1:
        return u"在职"
    elif value == 2:
        return u"离职"


@register.filter(name='format_date')
def format_date(value, format=settings.DATE_INPUT_FORMATS[1]):
    if isinstance(value, date):
        return value.strftime(format)
    else:
        return value


@register.filter(name='format_datetime')
def format_datetime(value, format=settings.DATETIME_INPUT_FORMATS[1]):
    if isinstance(value, datetime):
        return value.strftime(format)
    else:
        return value


@register.filter(name='selected_departments')
def selected_departments(departments, selected_departments):
    """是否为选中部门"""
    if not selected_departments:
        return False
    else:
        return str(departments) in selected_departments


@register.filter(name='get_dep_name_by_dep_id')
def get_dep_name_by_dep_id(dep_id):
    """
    根据部门id获取部门名。
    """
    department_name = ""
    dep_id_fix = dep_id[0:-1]
    departments_id = [int(i) for i in dep_id_fix.split(',')]

    departments = Department.objects.filter(id__in=departments_id)
    for department in departments:
        department_name = department_name+','+department.name
    return department_name[1:]


@register.filter(name='sub_datetime')
def sub_datetime(value, sub):
    return value - sub


@register.filter(name='get_name')
def get_name(value):
    user = User.objects.filter(personal_id=value).get()
    return user.full_name

@register.filter(name='get_group')
def get_group(value):
    user = User.objects.filter(personal_id=value).get()
    return user.groups.get().name