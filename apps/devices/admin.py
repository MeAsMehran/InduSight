from django.contrib import admin
from apps.devices.models import Device, DeviceType, DeviceLog


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('parameter', 'code', 'des')


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id' ,'get_device_type', 'time', 'value')

    def get_device_type(self, obj):
        return ", ".join([dt.parameter for dt in obj.device_type.all()])


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'des', 'get_device_types')
    filter_horizontal = ('device_type',)  # optional, for nicer form widget

    def get_device_types(self, obj):
        return ", ".join([dt.parameter for dt in obj.device_type.all()])


