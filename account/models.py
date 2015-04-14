#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.admindocs.utils import ROLES
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from django.forms import ModelForm, Form
from django import forms
from django.utils.translation import ugettext_lazy as _


class MyUserManage(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, is_active=True, is_superuser=False,
                          last_login=datetime.datetime.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(PermissionsMixin):
    username = models.CharField(_("username"), max_length=40, db_index=True, unique=True)
    create_datetime = models.DateTimeField(auto_now_add=True) #创建日期
    update_datetime = models.DateTimeField(auto_now=True) #更新日期
    full_name = models.CharField(_('full name'), max_length=20, ) #全名
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('date joined'), default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "username"
    objects = MyUserManage()
    REQUIRED_FIELDS = []

    def get_username(self):
        """Return the identifying username for this User"""
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return self.get_username(),

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password", "update_datetime"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_short_name(self):
        raise self.get_full_name()

    def get_full_name(self):
        return self.full_name if self.full_name else self.username

    def has_role(self, role):
        return role in ROLES and self.groups.filter(name=ROLES[role]).exists()

    class Meta:
        permissions = (
            ("view_user", u"能否查看用户"),
        )
        db_table = "hr_manage_account"
        # app_label = 'account'

    def __unicode__(self):
        return self.username


class UserForm(ModelForm):
    role = forms.IntegerField()
    cinema = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        # 添加模式下检查用户名是否唯一
        if 'username' in cleaned_data and 'mode' in cleaned_data:
            username = cleaned_data['username']
            if User.objects.filter(username=username).count() > 0:
                msg = u"用户名已存在。"
                self._errors["username"] = self.error_class([msg])

                del cleaned_data["username"]

        return cleaned_data


class UserEditForm(UserForm):
    city_id = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'full_name')


class UserLoginForm(Form):
    username = forms.CharField(required=True, max_length=30)
    password = forms.CharField(required=True, max_length=20)
    needRemember = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()

        if 'username' in cleaned_data and cleaned_data.has_key('password'):
            username = cleaned_data['username']
            password = cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    msg = u"该用户已禁用。"
                    self._errors["username"] = self.error_class([msg])
                    del cleaned_data["username"]
            else:
                msg = u"用户不存在或者密码不正确。"
                self._errors["password"] = self.error_class([msg])

                del cleaned_data["password"]

        return cleaned_data
