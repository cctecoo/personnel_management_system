#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.forms import ModelForm, Form, DateField, CharField
from django import forms
from django.utils.translation import ugettext_lazy as _


class Department(models.Model):
    """
    部门
    """
    name = models.CharField(u"名称", max_length=255)  # 公司名称
    description = models.CharField(u"部门描述", null=True, blank=True, max_length=255)  # 部门描述
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_comprehensive_department"


class DepartmentForm(ModelForm):
    """
    部门信息Form
    """
    mode = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(DepartmentForm, self).clean()

        # 检查数据有效性
        # 添加模式下检查名称是否唯一
        if 'name' in cleaned_data and 'mode' in cleaned_data:
        # if 'name' in cleaned_data :
            name = cleaned_data['name']
            if Department.objects.filter(name=name).count() > 0:
                msg = u"该名称已存在。"
                self._errors["name"] = self.error_class([msg])

                del cleaned_data["name"]
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ('name', 'description',)