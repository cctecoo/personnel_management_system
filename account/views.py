#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from account.models import User, UserForm, UserEditForm, UserLoginForm
from utility import role_manager
from utility.base_view import back_to_original_page, get_list_params
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_STAFF, ROLE_MANAGER, ROLE_HR, ROLES, ROLE_SYSADMIN, get_role_id


def login_view(request):
    """
    登录View
    """
    return render(request, "account/login.html", )


def login_action(request):
    """
    登录动作
    """
    form = UserLoginForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        if cleaned_data.has_key('needRemember') and cleaned_data['needRemember']:
            request.session.set_expiry(2678400)  # session保持一个月

        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        # Return an 'invalid login' error message.
        return back_to_original_page(request, "/")

    return render(request, "account/login.html", {
        "form": form,
    })


def logout_action(request):
    """
    注销动作
    """
    logout(request)
    return redirect(settings.LOGIN_URL)


@login_required
def user_add_view(request):
    """
    增加用户View
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = UserForm()
    return render(request, "account/add.html", {
        "form": form,
    })


@login_required
def user_add_action(request):
    """
    增加用户
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    form = UserForm(request.POST)

    if form.is_valid():
        role = form.cleaned_data['role']

        # 人事用户也能够新建用户，但是只能新建员工
        if check_role(request, ROLE_HR) and role != ROLE_STAFF:
            msg = u"人事只能新建普通员工。"
            form._errors["role"] = form.error_class([msg])
            return render(request, "account/add.html", {"form": form, })

        user = form.save()
        user.set_password(form.cleaned_data['password'])
        group = role_manager.get_role(role)
        if group:
            user.groups.add(group)
        user.save()
        return back_to_original_page(request, "/account/list/")
    else:
        return render(request, "account/add.html", {
            "form": form,
        })


@login_required
def user_list_view(request):
    """
    用户一览View
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    queryset = User.objects.filter(is_superuser=False).exclude(is_active=False)
    params = get_list_params(request)

    order_dict = {
        u"un": "username",
        u"fn": "full_name",
        u"cd": "create_datetime",
        u"gr": "groups",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(username__contains=params['query'])

    # 如果是经理，权限等同管理员，显示全部
    if check_role(request, ROLE_MANAGER):
        queryset = queryset
    # 如果是人事，只显示员工
    elif check_role(request, ROLE_HR):
        queryset = queryset.filter(groups__name=ROLES[ROLE_STAFF])

    # 排序
    if not params['order_field'] or not order_dict.has_key(params['order_field']):
        params['order_field'] = 'un'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "account/list.html", {
        "users": queryset[params['from']:params['to']],
        "query_params": params,
        "need_pagination": params['limit'] < total_count,
        "total_count": total_count,
    })


@login_required
def user_view_view(request, id):
    """
    编辑用户视图
    """
    user = get_object_or_404(User, id=id)
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    form = UserForm(instance=user)
    role_id = get_role_id(role_name) if role_name else None

    # 只能查看自己或者低于自己权限用户
    if check_role(request, ROLE_MANAGER) and ((role_id == ROLE_MANAGER and user.username != request.user.username)
                                              or user.is_superuser):
        raise PermissionDeniedError

    if check_role(request, ROLE_HR) and ((role_id == ROLE_HR and user.username != request.user.username)
                                         or role_id not in (ROLE_STAFF, ROLE_HR)):
        raise PermissionDeniedError

    if check_role(request, ROLE_STAFF) and user.username != request.user.username:
        raise PermissionDeniedError

    return render(request, "account/view.html", {
        "form": form,
        "role": role_id,
        "role_name": role_name,
    })
