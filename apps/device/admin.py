from django.contrib import admin
from device import models
from push_notifications import models as device_models
from push_notifications.admin import GCMDeviceAdmin

admin.site.unregister(device_models.APNSDevice)
admin.site.unregister(device_models.GCMDevice)
admin.site.unregister(device_models.WNSDevice)
admin.site.unregister(device_models.WebPushDevice)


@admin.register(models.FCMDevice)
class FCMDeviceAdmin(GCMDeviceAdmin):
    pass
