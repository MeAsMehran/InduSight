from apps.devices.models import DeviceLog
from rest_framework.exceptions import ValidationError


def params_validate(data):

    fields = []

    for field in DeviceLog._meta.concrete_fields:
        fields.append(field.name)


    
    # order_by Validations:
    order_by = data.get('order_by')

    if order_by:
        order_by = order_by.replace("-", "")

        if order_by not in fields:
            raise ValidationError({"order_by": f"Invalid field. Allowed values are: {', '.join(fields)}"})

    return data

