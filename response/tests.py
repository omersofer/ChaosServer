# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from response.models import Mode

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
    mode200ReqPercent = normal200ReqPercent
    mode401ReqPercent = normal401ReqPercent
    mode500ReqPercent = normal500ReqPercent
    if (chaos_mode == 1):  # degraded case
        mode200ReqPercent = degraded200ReqPercent
        mode401ReqPercent = degraded401ReqPercent
        mode500ReqPercent = degraded500ReqPercent
    elif (chaos_mode == 2):  # failure casse
        mode200ReqPercent = failure200ReqPercent
        mode401ReqPercent = failure401ReqPercent
        mode500ReqPercent = failure500ReqPercent
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
        change_chaos_mode(0)
        # check that get the required responses percentages
        probeResponseEndpoint(self, 0)

    def testDegradedModeResponses(self):
        # set chaos_mode=degraded
        change_chaos_mode(1)
        # check that get the required responses percentages
        probeResponseEndpoint(self, 1)

    def testFailureModeResponses(self):
        # set chaos_mode=failure
        change_chaos_mode(2)
        # check that get the required responses percentages
        probeResponseEndpoint(self, 2)
