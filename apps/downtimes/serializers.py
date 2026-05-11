from rest_framework import serializers
from apps.downtimes.models import Downtime
from apps.devices.models import Device
from django.utils import timezone
from rest_framework.exceptions import ValidationError


# Serializers

from apps.downtimes.validations.downtime_validate import downtime_validate
class DowntimeSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(write_only=True, required=True)
    time = serializers.DateTimeField(
        write_only=True,
        required=False,
        default=timezone.now
    )

    class Meta:
        model = Downtime
        fields = (
            'device_name',
            'device',
            'start',
            'finish',
            'duration',
            'reason',
            'time',
        )
        read_only_fields = ('device', 'start', 'finish', 'duration')

    def validate(self, attrs):
        return downtime_validate(data=attrs)

    
