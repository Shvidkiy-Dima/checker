from django.contrib import admin
from solo.admin import SingletonModelAdmin
from monitor.models import MonitorConfig, Monitor, MonitorLog


@admin.register(MonitorConfig)
class MonitorConfigAdmin(SingletonModelAdmin):
    pass


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'interval', 'last_request',
                    'created', 'is_active', 'user')


@admin.register(MonitorLog)
class MonitorLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'monitor_name', 'monitor_url',
                    'is_successful', 'response_code', 'created')

    def monitor_name(self, obj):
        return obj.monitor.name

    def monitor_url(self, obj):
        return obj.monitor.url