# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from response.models import Mode
from Chaos_Server import config


def normal(request):
    return change_chaos_mode(request, config.normalMode)


def degraded(request):
    return change_chaos_mode(request, config.degradedMode)


def failure(request):
    return change_chaos_mode(request, config.failureMode)


def change_chaos_mode(request, new_mode):
    if request.user.is_authenticated():
        mode = Mode.objects.get(id=1)
        mode.chaos_mode = new_mode
        mode.save()
        return HttpResponse(status=200)
    return HttpResponse(status=401)


