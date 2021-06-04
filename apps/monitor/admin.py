from django.contrib import admin
from solo.admin import SingletonModelAdmin
from monitor.models import MonitorConfig


@admin.register(MonitorConfig)
class MonitorConfigAdmin(SingletonModelAdmin):
    pass

