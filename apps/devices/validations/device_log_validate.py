from rest_framework.fields import ValidationError
from apps.devices.models import Device, DeviceType


def device_log_validate(data):
    
    device_name = data.get('device')  
    device_type_name = data.get('device_type')

    # Check if the device exists or not:
    if device_name:
        try:
            device = Device.objects.get(name=device_name)
        except Device.DoesNotExist:
            raise ValidationError("This device name doesn't exist!") 

    # Check if the device_type exists or not:
    if device_type_name:
        try:
            device_type = DeviceType.objects.get(parameter=device_type_name)
        except DeviceType.DoesNotExist:
            raise ValidationError("This device type name doesn't exist!")

    data['device'] = device

    device_type_ids = device.device_type.values_list('id', flat=True)

    # Check if the device type is availabe in the device's device types:
    if device_type.id in device_type_ids:
        data['device_type'] = device_type
    else:
        raise ValidationError("This device_type doesn't exist!")

    return data


