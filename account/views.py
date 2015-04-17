#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from account.models import User, UserForm, UserEditForm, UserLoginForm
from information.models import Personal
from utility import role_manager
from utility.base_view import back_to_original_page, get_list_params
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_STAFF, ROLE_MANAGER, ROLE_HR, ROLES, ROLE_SYSADMIN, get_role_id, \
    check_permission_allowed


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
        if not user.is_superuser:
            personal = Personal.objects.create()
            user.personal_id = personal.id
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
    查看用户视图
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    user = get_object_or_404(User, id=id)
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    form = UserForm(instance=user)
    role_id = get_role_id(role_name) if role_name else None

    return render(request, "account/view.html", {
        "form": form,
        "role": role_id,
        "role_name": role_name,
    })


@login_required
def user_delete_action(request):
    """
    删除用户
    """
    if check_role(request, ROLE_STAFF):
        raise PermissionDeniedError

    # if not request.POST.has_key('pk'):
    #     raise InvalidPostDataError()
    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        # if key and is_int(key):
        if key:
            pks.append(int(key))

    User.objects.filter(id__in=pks).update(is_active=False)
    return back_to_original_page(request, '/account/list/')


@login_required
def user_edit_view(request, id):
    """
    编辑用户视图
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    user = get_object_or_404(User, id=id)

    form = UserForm(instance=user)
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    else:
        role_name = None
    return render(request, "account/edit.html", {
        "form": form,
        "id": id,
        "role": get_role_id(role_name),
        "role_name": role_name,
        # "update_timestamp": crypt.encryt(unicode(user.update_datetime))
    })


@login_required
def user_edit_action(request):
    """
    编辑用户动作
    """
    # if not request.POST.has_key('id'):
    #     raise InvalidPostDataError()
    id = request.POST['id']

    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    user = get_object_or_404(User, id=id)

    if request.POST.has_key('password'):
        form = UserForm(request.POST, instance=user)
    else:
        form = UserEditForm(request.POST, instance=user)

    if form.is_valid():
        # 数据一致性校验
        # if not 'update_timestamp' in request.POST or crypt.loads(request.POST["update_timestamp"]) != unicode(
        #         user.update_datetime):
        #     raise DataExclusivityError()
        if request.user.is_superuser:
            role = form.cleaned_data['role']
            group = role_manager.get_role(role)
            if group:
                user.groups.clear()
                user.groups.add(group)
        user.full_name = form.cleaned_data['full_name']

        if not isinstance(form, UserEditForm):
            user.set_password(form.cleaned_data['password'])
            user.save(update_fields=("full_name", "password", "update_datetime"))
        else:
            user.save(update_fields=("full_name", "update_datetime"))

        # 员工没有访问list权限,所以这里返回index
        if check_role(request, ROLE_STAFF):
            return back_to_original_page(request, "/")
        return back_to_original_page(request, "/account/list/")
    else:
        role = form.cleaned_data['role'] if 'role' in form.cleaned_data else None
        return render(request, "account/edit.html", {
            "form": form,
            "id": id,
            "role": role,
            "role_name": ROLES[role] if role in ROLES else "",
            # "update_timestamp": crypt.encryt(unicode(user.update_datetime))
        })