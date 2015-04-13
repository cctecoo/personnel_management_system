#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def first_page(request):
    return HttpResponse("<p>account</p>")