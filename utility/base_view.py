#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import redirect

__author__ = 'cc'


# 返回之前的现场
def back_to_original_page(request, url="/"):
    if request.POST.has_key('redirect_url') and request.POST['redirect_url']:
        return redirect(request.POST['redirect_url'])
    else:
        return redirect(url)


# 获取一览表的参数
def get_list_params(request):
    fr = request.GET['fr'] if request.GET.has_key('fr') else None  # 记录起始条数
    lm = request.GET['lm'] if request.GET.has_key('lm') else None  # 显示记录条数
    od = request.GET['od'] if request.GET.has_key('od') else None  # 排序方向
    of = request.GET['of'] if request.GET.has_key('of') else ''  # 排序字段
    q = request.GET['q'] if request.GET.has_key('q') else ''  # 查询关键字

    # fr = 0 if fr is None or not is_int(fr) or int(fr) < 0 else int(fr)
    fr = 0 if fr is None or int(fr) < 0 else int(fr)
    # lm = settings.PAGINATION_LIMIT if lm is None or not is_int(lm) or int(lm) < 0 else int(lm)
    lm = 10 if lm is None or int(lm) < 0 else int(lm)
    to = fr + lm
    od = '' if od is None or od != '-' else '-'

    return {
        "from": fr,
        "limit": lm,
        "to": to,
        "order_direction": od,
        "order_field": of,
        "query": q,
    }