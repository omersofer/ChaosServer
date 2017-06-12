# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from response.models import Mode


def normal(request):
    return change_chaos_mode(request, 0)


def degraded(request):
    return change_chaos_mode(request, 1)


def failure(request):
    return change_chaos_mode(request, 2)


def change_chaos_mode(request, new_mode):
    if request.user.is_authenticated():
        mode = Mode.objects.get(id=1)
        mode.chaos_mode = new_mode
        mode.save()
        return HttpResponse(status=200)
    return HttpResponse(status=401)


