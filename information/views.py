#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from utility.exception import PermissionDeniedError
from utility.role_manager import check_permission_allowed


@login_required
def information_personal_view(request, id):
    """
    个人信息View
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    return render(request, "information/personal.html", {
    })