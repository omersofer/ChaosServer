# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Mode(models.Model):
    chaos_mode = models.IntegerField(default=0)

    def __str__(self):
        return "chaos_mode: " + str(self.chaos_mode)
