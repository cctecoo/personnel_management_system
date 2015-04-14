#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render

from account.models import User, UserForm, UserEditForm, UserLoginForm
from utility import role_manager
from utility.base_view import back_to_original_page


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
        "app_version": settings.APP_VERSION,
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
    form = UserForm()
    return render(request, "account/add.html", {
        "form": form,
    })


@login_required
def user_add_action(request):
    """
    增加用户
    """
    form = UserForm(request.POST)

    if form.is_valid():
        role = form.cleaned_data['role']

        user = form.save()
        user.set_password(form.cleaned_data['password'])
        group = role_manager.get_role(role)
        if group:
            user.groups.add(group)
        user.save()
        return back_to_original_page(request, "/")
    else:
        return render(request, "account/add.html", {
            "form": form,
        })
