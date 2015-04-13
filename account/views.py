#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render

from account.models import UserLoginForm
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