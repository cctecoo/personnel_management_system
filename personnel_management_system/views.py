#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from notice.models import Notice
from personnel_management_system import settings


@login_required
def index_view(request):
    """
    首页View
    """
    today = datetime.datetime.now().strftime(settings.DATETIME_INPUT_FORMATS[3])

    # 取出符合时间段的公告，按照创建时间倒序排（最新）
    queryset = Notice.objects.filter(start_date__lt=today, end_date__gt=today).\
        exclude(delete_flg=True).order_by("-create_datetime")

    # 非系统管理员 只能查看自己所属部门的公告
    if not request.user.is_superuser:
        str_department_id = str(request.user.personal.department.id)
        plus_department_id = str_department_id + ','
        queryset = queryset.filter(
            Q(dep_id__contains=plus_department_id) |
            Q(dep_id=str_department_id)
            )

    return render(request, "index/index.html", {
        "notices": queryset,

    })