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

from comprehensive.models import Department, DepartmentForm
from utility.base_view import get_list_params, back_to_original_page
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_STAFF


@login_required
def department_list_view(request):
    """
    部门一览View
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    queryset = Department.objects.filter(delete_flg=False).order_by('name')
    params = get_list_params(request)

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(username__contains=params['query'])

    total_count = queryset.count()

    return render(request, "comprehensive/department_list.html", {
        "departments": queryset,
        "query_params": params,
        "total_count": total_count,
    })


@login_required
def department_add_view(request):
    """
    增加部门View
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = DepartmentForm()
    return render(request, "comprehensive/department_add.html", {
        "form": form,
    })


@login_required
def department_add_action(request):
    """
    增加部门
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = DepartmentForm(request.POST)

    if form.is_valid():
        form.instance.name = request.POST['name']
        if request.POST['description']:
            form.instance.description = request.POST['description']

        form.save()
        return back_to_original_page(request, "/comprehensive/department/list/")
    else:
        return render(request, "comprehensive/department_add.html", {
            "form": form,
        })

@login_required
def department_edit_view(request, department_id):
    """
    编辑部门视图
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    department = get_object_or_404(Department, id=department_id)

    form = DepartmentForm(instance=department)

    return render(request, "comprehensive/department_edit.html", {
        "form": form,
        "department_id": department_id,
    })


@login_required
def department_edit_action(request):
    """
    编辑部门动作
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    department_id = request.POST['department_id']

    department = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST, instance=department)

    # form.cleaned_data['mode'] = request.POST['mode']
    if form.is_valid():
        form.instance.name = request.POST['name']
        if request.POST['description']:
            form.instance.description = request.POST['description']

        form.save()
        return back_to_original_page(request, "/comprehensive/department/list/")
    else:
        return render(request, "comprehensive/department_edit.html", {
            "form": form,
            "department_id": department_id,
        })