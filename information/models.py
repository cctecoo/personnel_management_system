#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.forms import ModelForm, Form, DateField, CharField
from django import forms
from django.utils.translation import ugettext_lazy as _

from comprehensive.models import Department
from utility.constant import PERSONAL_SEX_MALE, PERSONAL_STATUS_CHOICE, PERSONAL_STATUS_WORK


class Job(models.Model):
    """
    工作经历
    """
    start_date = models.DateField(u"开始日")  # 工作开始日
    end_date = models.DateField(u"结束日")  # 工作结束日
    company = models.CharField(u"公司名称", max_length=255)  # 公司名称
    position = models.CharField(u"职位", max_length=255)  # 职位
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_job"


class Education(models.Model):
    """
    教育经历
    """
    start_date = models.DateField(u"开始日")  # 开始日
    end_date = models.DateField(u"结束日")  # 结束日
    school = models.CharField(u"学校名称", max_length=255)  # 学校名称
    kind = models.CharField(u"种类", max_length=255)  # 种类
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_education"


class Family(models.Model):
    """
    家庭信息
    """
    name = models.CharField(u"名称", max_length=255)  # 名称
    relationship = models.CharField(u"关系", max_length=255)  # 关系
    mobile_phone = models.CharField(u'手机号', null=True, blank=True, max_length=100)  # 手机号
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_family"


class Personal(models.Model):
    """
    个人信息
    """
    sex = models.PositiveIntegerField(u"性别", default=PERSONAL_SEX_MALE)  # 性别
    birthday = models.DateField(u"出生年月", null=True, blank=True,)  # 出生年月
    phone = models.CharField(u'手机号', null=True, blank=True, max_length=100)  # 手机号
    status = models.PositiveSmallIntegerField(u"员工状态", blank=True, choices=PERSONAL_STATUS_CHOICE, default=PERSONAL_STATUS_WORK)  # 员工状态
    department = models.ForeignKey(Department, null=True, blank=True, related_name="belong_to_personal")  # 个人所属部门
    job = models.ManyToManyField(Job, null=True, blank=True, related_name="personal_job",
                                 db_table="hr_manage_information_personal_job_relationships")  # 工作经历
    education = models.ManyToManyField(Education, null=True, blank=True, related_name="personal_education",
                                       db_table="hr_manage_information_personal_education_relationships")  # 教育经历
    family = models.ManyToManyField(Family, null=True, blank=True, related_name="personal_family",
                                    db_table="hr_manage_information_personal_family_relationships")  # 家庭信息
    create_datetime = models.DateTimeField(auto_now_add=True)  # 创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = "hr_manage_information_personal"


class PersonalForm(ModelForm):
    """
    个人信息Form
    """

    def clean(self):
        cleaned_data = super(PersonalForm, self).clean()

        # 检查数据有效性
        # 手机号必须为数字
        if 'phone' in cleaned_data:
            phone = cleaned_data['phone']
            if phone != "" and not phone.isdigit():
                msg = u"请确认手机号全部为数字。"
                self._errors["phone"] = self.error_class([msg])
                del cleaned_data["phone"]

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Personal
        fields = ('sex', 'birthday', 'phone',)


class PersonalDepartmentForm(ModelForm):
    """
    个人所属部门Form
    """
    def clean(self):
        cleaned_data = super(PersonalDepartmentForm, self).clean()
        # 检查数据有效性
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PersonalDepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Personal
        fields = ('department',)


class PersonalStatusForm(ModelForm):
    """
    个人状态Form
    """
    def clean(self):
        cleaned_data = super(PersonalStatusForm, self).clean()
        # 检查数据有效性
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PersonalStatusForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Personal
        fields = ('status',)


class JobForm(ModelForm):
    """
    工作经历Form
    """

    def clean(self):
        cleaned_data = super(JobForm, self).clean()

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
        super(JobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = ('start_date', 'end_date', 'company', 'position',)


class EducationForm(ModelForm):
    """
    教育经历Form
    """

    def clean(self):
        cleaned_data = super(EducationForm, self).clean()

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
        super(EducationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Education
        fields = ('start_date', 'end_date', 'school', 'kind',)


class FamilyForm(ModelForm):
    """
    家庭信息Form
    """

    def clean(self):
        cleaned_data = super(FamilyForm, self).clean()

        # 检查数据有效性
        # 手机号必须为数字
        if 'mobile_phone' in cleaned_data:
            mobile_phone = cleaned_data['mobile_phone']
            if mobile_phone != "" and not mobile_phone.isdigit():
                msg = u"请确认手机号全部为数字。"
                self._errors["mobile_phone"] = self.error_class([msg])
                del cleaned_data["mobile_phone"]

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Family
        fields = ('name', 'relationship', 'mobile_phone',)