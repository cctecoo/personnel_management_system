#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, date
import time
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext

from account.models import User, UserForm
from information.models import Personal, PersonalForm, Job, JobForm
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

    # 工作信息
    job_count = personal.job.filter(delete_flg=False).count()
    job_list = personal.job.filter(delete_flg=False).order_by("start_date")

    return render(request, "information/personal.html", {
        "id": id,
        "full_name": user.full_name,
        "role_name": role_name,
        "form": personal,
        "job_count": job_count,
        "job_list": job_list,
    })


@login_required
def information_personal_edit_action(request, id):
    """
    编辑个人信息action
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError
    response_data = {}
    queryset = Personal.objects.filter(belong_to__id=id).get()
    form = PersonalForm(request.POST, instance=queryset)

    if form.is_valid():
        form.instance.sex = request.POST['sex']
        form.save()

        response_data['validation'] = True
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    else:
        response_data['validation'] = False
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def job_add_view(request, user_pk):
    """
    添加工作view
    """
    if not check_permission_allowed(request, user_pk):
        raise PermissionDeniedError
    # 生成工作Form对象实例
    jobForm = JobForm()

    return render_to_response("information/job_edit.html", {
        'result': 'OK',
        'user_pk': user_pk,
        'job': jobForm,
    }, context_instance=RequestContext(request))


@login_required
def job_edit_view(request, user_pk, job_id):
    """
    编辑工作view
    """
    if not check_permission_allowed(request, user_pk):
        raise PermissionDeniedError
    # 个人信息id
    user_id = int(user_pk)
    # 工作信息id
    job_id = int(job_id)

    # 取得个人信息
    queryset = Personal.objects.filter(belong_to__id=user_id, delete_flg=False)
    personal = queryset.get()

    # 取得工作信息
    queryset = personal.job.filter(id=job_id, delete_flg=False)
    job = queryset.get()

    # 生成工作信息对应的Form实例
    jobForm = JobForm(instance=job)

    return render_to_response("information/job_edit.html", {
        'result': 'OK',
        'user_pk': user_pk,
        'job': jobForm,
    }, context_instance=RequestContext(request))


@login_required
def job_edit_action(request, user_pk):
    """
    编辑工作action
    """
    if not check_permission_allowed(request, user_pk):
        raise PermissionDeniedError
    # 个人信息id
    user_id = int(user_pk)

    # 取得请求的工作信息id
    id = request.POST['id']

    if id == "":
        # 取得工作信息的Form实例
        form = JobForm(request.POST, instance=Job())
    else:
        # 取得工作信息
        queryset = Job.objects.filter(id__exact=int(id), delete_flg=False)
        job = queryset.get()
        # 生成工作信息对应的Form实例
        form = JobForm(request.POST, instance=job)

    if form.is_valid():
        if id == "":
            # 取得个人信息
            queryset = Personal.objects.filter(belong_to__id=user_id, delete_flg=False)
            personal = queryset.get()
            # 保存
            job = form.save()
            # 在个人信息中保存工作信息，既保存relationship
            personal.job.add(job)

        else:
            # 保存
            form.save()

        return render_to_response("information/job_edit.html", {
            'result': 'OK',
            'job_validation': True,
            'user_pk': user_pk,
            'job': form,
        }, context_instance=RequestContext(request))

    else:
        return render_to_response("information/job_edit.html", {
            'result': 'OK',
            'job_validation': False,
            'user_pk': user_pk,
            'job': form,
        }, context_instance=RequestContext(request))


@login_required
def job_list_view(request, user_pk):
    """
    工作一览View
    """
    if not check_permission_allowed(request, user_pk):
        raise PermissionDeniedError
    # 个人信息id
    user_id = int(user_pk)
    # 取得个人信息
    queryset = Personal.objects.filter(belong_to__id=user_id, delete_flg=False)
    personal = queryset.get()

    # 工作信息
    job_count = personal.job.filter(delete_flg=False).count()
    job_list = personal.job.filter(delete_flg=False).order_by("start_date")

    return render_to_response("information/job_list.html", {
        'result': 'OK',
        'user_pk': user_pk,
        'job_count': job_count,
        'job_list': job_list,
    }, context_instance=RequestContext(request))


@login_required
def job_delete_action(request, user_pk):
    """
    删除工作action
    """
    if not check_permission_allowed(request, user_pk):
        raise PermissionDeniedError
    # 个人信息id
    user_id = int(user_pk)

    pks = []
    for key in request.POST["job_pks"].split(','):
        # if key and is_int(key):
        if key:
            pks.append(int(key))

    # 取得工作信息
    queryset = Job.objects.filter(id__in=pks, delete_flg=False)

    # 将工作信息逻辑删除
    queryset.update(delete_flg=True, update_datetime=datetime.now())

    # 取得个人信息
    queryset = Personal.objects.filter(belong_to__id=user_id, delete_flg=False)
    personal = queryset.get()

    # 工作信息
    job_count = personal.job.filter(delete_flg=False).count()
    job_list = personal.job.filter(delete_flg=False).order_by("start_date")

    return render_to_response("information/job_list.html", {
        'result': 'OK',
        'user_pk': user_pk,
        'job_count': job_count,
        'job_list': job_list,
    }, context_instance=RequestContext(request))
