# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from response.models import Mode
from random import randint


def index(request):
    mode = Mode.objects.get(id=1)
    rand = (randint(1,100))

    #"normal" mode: 100% of requests will result in 200 http responses
    if mode.chaos_mode == 0:
        return HttpResponse(status=200)

    #"degraded" mode:   50% of requests will result in 200 http responses
    #                   25% of requests will result in 401 http responses
    #                   25% of requests will result in 500 http responses
    elif mode.chaos_mode == 1:
        if rand <= 50:
            return HttpResponse(status=200)
        elif rand <= 75:
            return HttpResponse(status=401)
        else:
            return HttpResponse(status=500)

    #"failure" mode:    5%  of requests will result in 200 http responses
    #                   95% of requests will result in 500 http responses
    else:
        if rand <= 5:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
