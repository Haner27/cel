# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import Task


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass