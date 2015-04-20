#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
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

        # return render_to_response("information/personal.html", {
        #     'result': 'OK',
        #     'validation': True,
        #     'form': form,
        # },  context_instance=RequestContext(request))
        response_data['validation'] = True
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    else:
        # return render_to_response("information/personal.html", {
        #     'result': 'OK',
        #     'validation': False,
        #     'form': form,
        # },  context_instance=RequestContext(request))
        response_data['validation'] = False
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def job_add_view(request, personal_pk):
    """
    添加工作view
    """
    # 生成工作Form对象实例
    jobForm = JobForm()

    return render_to_response("information/job_edit.html", {
        'result': 'OK',
        'personal_pk': personal_pk,
        'job': jobForm,
    }, context_instance=RequestContext(request))


@login_required
def job_edit_action(request, personal_pk):
    """
    编辑工作action
    """
    # response_data = {}

    # 个人信息id
    personal_id = int(personal_pk)

    # 取得请求的工作id
    id = request.POST['id']

    if id == "":
        # 取得工作信息
        form = JobForm(request.POST, instance=Job())

    else:
        # 取得工作信息
        queryset = Job.objects.filter(id__exact=int(id), delete_flg=False)
        # # 不存在，返回失败。
        # if queryset.count() == 0:
        #     response_data['result'] = 'fail'
        #     response_data['error_code'] = JSON_ERROR_CODE_DATA_NOT_EXIST
        #     response_data['error_msg'] = JSON_ERROR_MSG_GOODS_NOT_EXIST
        #     return HttpResponse(json.dumps(response_data), mimetype="application/json")
        # # 商品存在，取得商品对象实例
        job = queryset.get()
        # 生成工作实例对应的Form实例
        form = JobForm(request.POST, instance=job)

    if form.is_valid():
        if id == "":
            # 取得人员信息
            queryset = Personal.objects.filter(id__exact=personal_id, delete_flg=False)
            # # 活动不存在，返回失败。
            # if queryset.count() == 0:
            #     response_data['result'] = 'fail'
            #     response_data['error_code'] = JSON_ERROR_CODE_DATA_NOT_EXIST
            #     response_data['error_msg'] = JSON_ERROR_MSG_ACTIVITY_NOT_EXIST
            #     return HttpResponse(json.dumps(response_data), mimetype="application/json")
            # # 活动存在，取得活动对象实例
            personal = queryset.get()

            # 保存
            job = form.save()
            # 在活动中保存商品
            personal.job.add(job)

        else:
            # 保存
            form.save()

        return render_to_response("information/job_edit.html", {
            'result': 'OK',
            'job_validation': True,
            'personal_pk': personal_pk,
            'job': form,
        }, context_instance=RequestContext(request))

    else:
        return render_to_response("information/job_edit.html", {
            'result': 'OK',
            'job_validation': False,
            'personal_pk': personal_pk,
            'job': form,
        }, context_instance=RequestContext(request))


@login_required
def job_list_view(request, personal_pk):
    """
    工作一览View
    """
    # response_data = {}

    # 个人信息id
    personal_id = int(personal_pk)
    # 取得人员信息
    queryset = Personal.objects.filter(id__exact=personal_id, delete_flg=False)
    # # 活动不存在，返回失败。
    # if queryset.count() == 0:
    #     response_data['result'] = 'fail'
    #     response_data['error_code'] = JSON_ERROR_CODE_DATA_NOT_EXIST
    #     response_data['error_msg'] = JSON_ERROR_MSG_ACTIVITY_NOT_EXIST
    #     return HttpResponse(json.dumps(response_data), mimetype="application/json")
    # # 活动存在，取得活动对象实例
    personal = queryset.get()

    # 工作信息
    job_count = personal.job.filter(delete_flg=False).count()
    job_list = personal.job.filter(delete_flg=False).order_by("start_date")

    return render_to_response("information/job_list.html", {
        'result': 'OK',
        'personal_pk': personal_pk,
        'job_count': job_count,
        'job_list': job_list,
    }, context_instance=RequestContext(request))
