from rest_framework.fields import ValidationError
from apps.devices.models import Device, DeviceType


def device_log_validate(data):
    device_name = data.get('device')
    device_type_parameter = data.get('device_type')
    value = data.get('value')

    try:
        device = Device.objects.get(name=device_name)
    except Device.DoesNotExist:
        raise ValidationError("This device name doesn't exist!")

    device_type = device.device_type.filter(parameter=device_type_parameter)

    if not device_type.exists():
        raise ValidationError(
            "This device does not support the given device type parameter."
        )

    device_type = device_type.first()

    data['device'] = device
    data['device_type'] = device_type

    return data


