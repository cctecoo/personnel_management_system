#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect

__author__ = 'cc'

#返回之前的现场
def back_to_original_page(request, url = "/"):
    if request.POST.has_key('redirect_url') and request.POST['redirect_url']:
        return redirect(request.POST['redirect_url'])
    else:
        return redirect(url)