#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.forms import ModelForm, Form
from django import forms
from django.utils.translation import ugettext_lazy as _

from utility.constant import PERSONAL_SEX_MALE


class Personal(models.Model):
    """
    个人信息
    """
    sex = models.PositiveIntegerField(u"性别", default=PERSONAL_SEX_MALE)  # 性别
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期

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