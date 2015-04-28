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

from account.models import User
from comprehensive.models import Department, DepartmentForm
from information.models import Personal, PersonalForm, PersonalDepartmentForm
from utility.base_view import get_list_params, back_to_original_page
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_STAFF, ROLE_MANAGER, ROLE_HR, ROLES


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
        queryset = queryset.filter(name__contains=params['query'])

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
    增加部门action
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


@login_required
def department_delete_action(request):
    """
    删除部门
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        # if key and is_int(key):
        if key:
            pks.append(int(key))

    Department.objects.filter(id__in=pks).update(delete_flg=True)
    return back_to_original_page(request, '/comprehensive/department/list/')


@login_required
def department_set_view(request):
    """
    部门配置view
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    user = User.objects.filter(is_superuser=False).exclude(is_active=False)
    # 如果是经理，权限等同管理员，显示全部
    if check_role(request, ROLE_MANAGER):
        user = user
    # 如果是人事，只显示员工
    elif check_role(request, ROLE_HR):
        user = user.filter(groups__name=ROLES[ROLE_STAFF])

    total_count = user.count()

    department = Department.objects.filter(delete_flg=False).order_by('name')

    return render(request, "comprehensive/department_set.html", {
        "form_list": user,
        "departments": department,
        "total_count": total_count,
    })


@login_required
def department_set_edit_action(request):
    """
    部门配置
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    response_data = {}
    personal_id = request.POST.get('personal_id')
    department_id = request.POST.get('department_id')

    queryset = Personal.objects.filter(id=personal_id).get()
    form = PersonalDepartmentForm(request.POST, instance=queryset)

    if form.is_valid():
        form.instance.department_id = department_id
        form.save()

        response_data['validation'] = True
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    else:
        response_data['validation'] = False
        return HttpResponse(json.dumps(response_data), mimetype="application/json")