from django.db import models
from apps.devices.models import Device, DeviceType
from django.core.exceptions import ValidationError

# Create your models here.

SITUATION = (
    ('above_max', 'Above Max'),
    ('below_min', 'Below Min'),
)

class Threshold(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='thresholds') 
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='thresholds') 
    min_value = models.FloatField(default=0) 
    max_value = models.FloatField(default=0) 
    active = models.BooleanField(default=False) 


    def clean(self):
        if self.min_value >= self.max_value:
            raise ValidationError(
                "min_value must be less than max_value"
            )
        # ensure the chosen device_type is actually assigned to the device
        if self.device and self.device_type:
            if not self.device.device_type.filter(id=self.device_type.id).exists():
                raise ValidationError(
                    {'device_type': "Selected device_type is not assigned to this device."}
                )

    def __str__(self):
        return f"Threshold for {self.device}"


class Alert(models.Model):
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts')
    device_type = models.ForeignKey(DeviceType, on_delete=models.SET_NULL, null=True, blank=True)
    threshold = models.ForeignKey(Threshold, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.FloatField(default=0) 
    situation = models.CharField(choices=SITUATION, max_length=20) 
    message = models.CharField(max_length=255,)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.device and self.device_type:
            if not self.device.device_type.filter(
                id=self.device_type.id
            ).exists():
                raise ValidationError(
                    "Selected device_type is not assigned to this device."
                )

    def save(self, *args, **kwargs):
        if self.device and not self.device_type:
            # pick one device_type as snapshot (business decision)
            self.device_type = self.device.device_type.first()
        super().save(*args, **kwargs)

    @property
    def is_above_max(self):
        return self.situation == 'above_max'

    @property
    def is_below_min(self):
        return self.situation == 'below_min'

    def __str__(self):
        return f"Alert(device={self.device}, value={self.value}, situation={self.situation})"


