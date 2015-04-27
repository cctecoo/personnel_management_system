#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, date
import time
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext

from comprehensive.models import Department
from notice.models import Notice, NoticeForm
from utility.base_view import get_list_params, back_to_original_page
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_STAFF


@login_required
def notice_list_view(request):
    """
    公告一览view
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    queryset = Notice.objects.filter().exclude(delete_flg=True)
    params = get_list_params(request)

    order_dict = {
        u"sd": "start_date",
        u"ed": "end_date",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(
            Q(content__contains=params['query']) |
            Q(title__contains=params['query'])
        )

    # 排序
    if not params['order_field'] or not order_dict.has_key(params['order_field']):
        params['order_field'] = 'sd'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "notice/list.html", {
        "notices": queryset[params['from']:params['to']],
        "query_params": params,
        "need_pagination": params['limit'] < total_count,
        "total_count": total_count,
    })


@login_required
def notice_add_view(request):
    """
    增加公告View
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = NoticeForm()
    departments = Department.objects.filter(delete_flg=False)

    return render(request, "notice/add.html", {
        "form": form,
        "departments": departments,
        "departments_need": True,
    })


@login_required
def notice_add_action(request):
    """
    增加部门action
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = NoticeForm(request.POST, instance=Notice())

    if form.is_valid() and 'dep_id' in request.POST:
        dep_id = ','.join(dict(request.POST)['dep_id'])

        form.instance.title = request.POST['title']
        form.instance.start_date = request.POST['start_date']
        form.instance.end_date = request.POST['end_date']
        form.instance.content = request.POST['content']
        form.instance.dep_id = dep_id

        form.save()
        return back_to_original_page(request, "/notice/list/")
    else:
        departments = Department.objects.filter(delete_flg=False)
        return render(request, "notice/add.html", {
            "form": form,
            "departments": departments,
            "departments_need": 'dep_id' in request.POST,
        })


@login_required
def notice_edit_view(request, notice_id):
    """
    编辑公告视图
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    notice = get_object_or_404(Notice, id=notice_id)

    form = NoticeForm(instance=notice)
    departments = Department.objects.filter(delete_flg=False)
    return render(request, "notice/edit.html", {
        "form": form,
        "notice_id": notice_id,
        "departments": departments,
        "departments_need": True,
    })


@login_required
def notice_edit_action(request):
    """
    编辑公告动作
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    notice_id = request.POST['notice_id']
    notice = get_object_or_404(Notice, id=notice_id)
    form = NoticeForm(request.POST, instance=notice)

    if form.is_valid():
        dep_id = ','.join(dict(request.POST)['dep_id'])

        form.instance.title = request.POST['title']
        form.instance.start_date = request.POST['start_date']
        form.instance.end_date = request.POST['end_date']
        form.instance.content = request.POST['content']
        form.instance.dep_id = dep_id

        form.save()

        return back_to_original_page(request, "/notice/list/")
    else:
        departments = Department.objects.filter(delete_flg=False)
        return render(request, "notice/edit.html", {
            "form": form,
            "notice_id": notice_id,
            "departments": departments,
            "departments_need": 'dep_id' in request.POST,
        })


@login_required
def notice_delete_action(request):
    """
    删除公告
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        # if key and is_int(key):
        if key:
            pks.append(int(key))

    Notice.objects.filter(id__in=pks).update(delete_flg=True)
    return back_to_original_page(request, '/notice/list/')


@login_required
def notice_view_view(request, notice_id):
    """
    查看公告
    """
    # 只能查看自己所属部门的公告，待完善

    notice = get_object_or_404(Notice, id=notice_id)
    form = NoticeForm(instance=notice)

    return render(request, "notice/view.html", {
        "form": form,
        "notice_id": notice_id,
    })