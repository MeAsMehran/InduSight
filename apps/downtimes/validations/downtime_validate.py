from rest_framework.exceptions import ValidationError
from apps.devices.models import Device

def downtime_validate(data):
    device_name = data.pop('device_name')
    time = data.get('time')

    if not device_name:
        raise ValidationError("Please Enter the device name!")
    
    if not time:
        raise ValidationError("Please Set the time!")
        
    try:
        data['device'] = Device.objects.get(name=device_name)
    except Device.DoesNotExist:
        raise ValidationError("No Device Found!")

    return data
    

