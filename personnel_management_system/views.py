#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response


# @login_required
def index_view(request):
    """
    首页View
    """
    now = datetime.datetime.now()

    return render_to_response('index/index.html', {'current_now': now})