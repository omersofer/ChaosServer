# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from response.models import Mode
from Chaos_Server import config

oneSideDelta = 10

# Help functions
def change_chaos_mode(new_mode):
    mode = Mode.objects.get(id=1)
    mode.chaos_mode = new_mode
    mode.save()


def probeResponseEndpoint(self, chaos_mode):
    http200Count = 0
    http401Count = 0
    http500Count = 0
    for a in range(0, 100):
        response = self.client.get('/response/')
        if response.status_code == 200:
            http200Count += 1
        if response.status_code == 401:
            http401Count += 1
        if response.status_code == 500:
            http500Count += 1
    # Set required percentages according to chaos_mode
    mode200ReqPercent = config.normal200ReqPercent
    mode401ReqPercent = config.normal401ReqPercent
    mode500ReqPercent = config.normal500ReqPercent
    if chaos_mode == config.degradedMode:  # degraded case
        mode200ReqPercent = config.degraded200ReqPercent
        mode401ReqPercent = config.degraded401ReqPercent
        mode500ReqPercent = config.degraded500ReqPercent
    elif chaos_mode == config.failureMode:  # failure case
        mode200ReqPercent = config.failure200ReqPercent
        mode401ReqPercent = config.failure401ReqPercent
        mode500ReqPercent = config.failure500ReqPercent
    # Check percent of each http response is in a reasonable delta from required percentages
    self.assertTrue((http200Count > (mode200ReqPercent-oneSideDelta)) and (http200Count < (mode200ReqPercent+oneSideDelta)))
    self.assertTrue((http401Count > (mode401ReqPercent-oneSideDelta)) and (http401Count < (mode401ReqPercent+oneSideDelta)))
    self.assertTrue((http500Count > (mode500ReqPercent-oneSideDelta)) and (http500Count < (mode500ReqPercent+oneSideDelta)))


# Test class
class ResponseTestCase(TestCase):
    def setUp(self):
        Mode.objects.create()

    def testNormalModeResponses(self):
        # Set chaos_mode=normal
        change_chaos_mode(config.normalMode)
        # check that get the required responses percentages
        probeResponseEndpoint(self, config.normalMode)

    def testDegradedModeResponses(self):
        # set chaos_mode=degraded
        change_chaos_mode(config.degradedMode)
        # check that get the required responses percentages
        probeResponseEndpoint(self, config.degradedMode)

    def testFailureModeResponses(self):
        # set chaos_mode=failure
        change_chaos_mode(config.failureMode)
        # check that get the required responses percentages
        probeResponseEndpoint(self, config.failureMode)
