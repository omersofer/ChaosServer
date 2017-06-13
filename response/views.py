# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from response.models import Mode
from random import randint

# Global variables
normal200ReqPercent = 100
normal401ReqPercent = 0
normal500ReqPercent = 0

degraded200ReqPercent = 50
degraded401ReqPercent = 25
degraded500ReqPercent = 25

failure200ReqPercent = 5
failure401ReqPercent = 0
failure500ReqPercent = 95


def index(request):
    mode = Mode.objects.get(id=1)
    rand = (randint(1,100))

    # "normal" mode: 100% of requests will result in 200 http responses
    if mode.chaos_mode == 0:
        return HttpResponse(status=200)

    # "degraded" mode:   50% of requests will result in 200 http responses
    #                    25% of requests will result in 401 http responses
    #                    25% of requests will result in 500 http responses
    elif mode.chaos_mode == 1:
        if rand <= degraded200ReqPercent:
            return HttpResponse(status=200)
        elif rand <= (degraded200ReqPercent+degraded401ReqPercent):
            return HttpResponse(status=401)
        else:
            return HttpResponse(status=500)

    # "failure" mode:    5%  of requests will result in 200 http responses
    #                   95% of requests will result in 500 http responses
    else:
        if rand <= failure200ReqPercent:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
