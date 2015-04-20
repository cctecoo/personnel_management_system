#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.forms import ModelForm, Form, DateField, CharField
from django import forms
from django.utils.translation import ugettext_lazy as _

from utility.constant import PERSONAL_SEX_MALE


class Job(models.Model):
    """
    工作经历
    """
    start_date = models.DateField(u"开始日")  # 工作开始日
    end_date = models.DateField(u"结束日")  # 工作结束日
    company = models.CharField(u"公司名称", max_length=255, blank=True, null=True)  # 公司名称
    position = models.CharField(u"职位", max_length=255, blank=True, null=True)  # 职位
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_job"


class Personal(models.Model):
    """
    个人信息
    """
    sex = models.PositiveIntegerField(u"性别", default=PERSONAL_SEX_MALE)  # 性别
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    job = models.ManyToManyField(Job, null=True, blank=True, related_name="personal_job",
                                 db_table="hr_manage_information_personal_job_relationships")  # 工作经历
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_personal"


class PersonalForm(ModelForm):
    """
    个人信息Form
    """

    def clean(self):
        cleaned_data = super(PersonalForm, self).clean()

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Personal
        fields = ('sex', )


class JobForm(ModelForm):
    """
    工作经历Form
    """

    def clean(self):
        cleaned_data = super(JobForm, self).clean()

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = ('start_date', 'end_date', 'company', 'position',)