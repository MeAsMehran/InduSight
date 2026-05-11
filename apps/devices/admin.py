
from django.contrib import admin
from apps.devices.models import Device, DeviceType, DeviceLog


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'parameter', 'code', 'des')


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'device_type', 'time', 'value')

    
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'des', 'get_device_types', 'get_supervisors')
    filter_horizontal = ('device_type', 'supervisor')


    def get_device_types(self, obj):
        return ", ".join(
            dt.parameter for dt in obj.device_type.all()
        )
    get_device_types.short_description = "Device Types"

    def get_supervisors(self, obj):
        return ", ".join(
            str(user.phone_number)
            for user in obj.supervisor.all()
        )
    get_supervisors.short_description = "Supervisors"


