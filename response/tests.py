# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from response.models import Mode


def change_chaos_mode(new_mode):
    mode = Mode.objects.get(id=1)
    mode.chaos_mode = new_mode
    mode.save()


class ResponseTestCase(TestCase):
    def setUp(self):
        Mode.objects.create()

    def testNormalModeResponses(self):
        # set chaos_mode=normal
        change_chaos_mode(0)
        http200Count = 0
        for a in range(0, 100):
            response = self.client.get('/response/')
            if response.status_code == 200:
                http200Count += 1
        # Check that all responses are 200 http responses
        self.assertTrue(http200Count == 100)

    def testDegradedModeResponses(self):
        # set chaos_mode=degraded
        change_chaos_mode(1)
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
        # Check number of each http response
        self.assertTrue(http200Count > 40 and http200Count < 60) # should be 50, check that in a reasonable range
        self.assertTrue(http401Count > 15 and http401Count < 35) # should be 25, check that in a reasonable range
        self.assertTrue(http500Count > 15 and http500Count < 35) # should be 25, check that in a reasonable range

    def testFailureModeResponses(self):
        # set chaos_mode=failure
        change_chaos_mode(2)
        http200Count = 0
        http500Count = 0
        for a in range(0, 100):
            response = self.client.get('/response/')
            if response.status_code == 200:
                http200Count += 1
            if response.status_code == 500:
                http500Count += 1
        # Check number of each http response
        self.assertTrue(http200Count < 15) #should be 5, check that in a reasonable range
        self.assertTrue(http500Count > 85) #should be 95, check that in a reasonable range
