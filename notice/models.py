#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.forms import ModelForm, Form, DateField, CharField
from django import forms
from django.utils.translation import ugettext_lazy as _


class Notice(models.Model):
    """
    公告
    """
    title = models.CharField(u'标题', max_length=255)  # 标题
    start_date = models.DateTimeField(u"开始日")  # 开始日期
    end_date = models.DateTimeField(u"结束日")  # 结束日期
    content = models.TextField(u'内容')  # 内容
    dep_id = models.CharField(u'所选通知部门', max_length=255)  # 所选通知部门（逻辑外键，多个dep_id以逗号分隔存放）
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_notice"


class NoticeForm(ModelForm):
    """
    公告Form
    """

    def clean(self):
        cleaned_data = super(NoticeForm, self).clean()

        # 检查数据有效性
        # 结束日期不能小于开始日期
        if 'end_date' in cleaned_data:
            start_date = cleaned_data['start_date']
            end_date = cleaned_data['end_date']
            if end_date <= start_date:
                msg = u"结束日期不能小于等于开始日期"
                self._errors["end_date"] = self.error_class([msg])
                del cleaned_data["end_date"]

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Notice
        fields = ('title', 'start_date', 'end_date', 'content', 'dep_id',)