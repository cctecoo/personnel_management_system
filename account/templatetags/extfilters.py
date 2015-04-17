#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'cc'
from datetime import date

from django import template
from django.db import connection
from django.template.defaultfilters import register
from django.utils.encoding import force_unicode
from django.conf import settings


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


@register.filter(name='format_date')
def format_date(value):
    if isinstance(value, date):
        return value.strftime(settings.DATE_INPUT_FORMATS[1])
    else:
        return value