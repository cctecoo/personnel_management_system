#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from account.models import User, UserForm
from information.models import Personal, PersonalForm
from utility.exception import PermissionDeniedError
from utility.role_manager import check_permission_allowed


@login_required
def information_personal_view(request, id):
    """
    个人信息View
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    # user = get_object_or_404(User, id=id)
    user = User.objects.filter(id=id).get()
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name

    personal = Personal.objects.filter(belong_to__id=id).get()
    return render(request, "information/personal.html", {
        "id": id,
        "full_name": user.full_name,
        "role_name": role_name,
        "form": personal,
    })


def information_personal_edit_action(request, id):
    """
    编辑个人信息action
    """
    queryset = Personal.objects.filter(belong_to__id=id).get()
    form = PersonalForm(request.POST, instance=queryset)

    if form.is_valid():

        form.instance.sex = request.POST['sex']
        form.save()

        return render_to_response("information/personal.html", {
            'result': 'OK',
            'validation': True,
            'form': form,
        })

    else:
        return render_to_response("information/personal.html", {
            'result': 'OK',
            'validation': False,
            'form': form,
        })

