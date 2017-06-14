# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from response.models import Mode
from Chaos_Server import config


class AdminPanelTestCase(TestCase):
    def setUp(self):
        Mode.objects.create()
        # log in as an admin (for is_authenticated() check)
        self.client = Client()
        self.my_admin = User(username='admin', is_staff=True)
        self.my_admin.set_password('adminadmin')  # can't set above because of hashing
        self.my_admin.save()  # save to temporary test db
        response = self.client.get('/admin/', follow=True)
        loginresponse = self.client.login(username='admin', password='adminadmin')
        self.assertTrue(loginresponse)  # check that logged in

    def testChaosModeChanges(self):
        # Test changing chaos_mode to "failure" (admin_panel.views.failure)
        response = self.client.get('/admin/failure/')
        self.assertEqual(Mode.objects.get(id=1).chaos_mode, config.failureMode)
        # Test changing chaos_mode to "degraded" (admin_panel.views.degraded)
        response = self.client.get('/admin/degraded/')
        self.assertEqual(Mode.objects.get(id=1).chaos_mode, config.degradedMode)
        # Test changing chaos_mode to "normal" (admin_panel.views.normal)
        response = self.client.get('/admin/normal/')
        self.assertEqual(Mode.objects.get(id=1).chaos_mode, config.normalMode)




