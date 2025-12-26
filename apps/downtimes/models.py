from django.db import models
from apps.devices.models import Device
from django.utils import timezone
from rest_framework.exceptions import ValidationError

# Create your models here.



class Downtime(models.Model):

    REASON = (
    ('periodic_maintenance', 'Periodic Maintenance'),
    ('hardware_failure', 'Hardware Failure'),
    ('system_update', 'System Update'),
    )
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='downtimes') 
    start = models.DateTimeField(null=False)
    finish = models.DateTimeField(null=True, blank=True) 
    duration = models.DurationField(null=True, blank=True)
    reason = models.CharField(max_length=512, choices=REASON, blank=False, null=False)

    def __str__(self):
        return self.device.name


    def save(self, *args, **kwargs):

        # Prevent multiple active downtimes
        if not self.pk:
            if Downtime.objects.filter(
                device=self.device,
                finish__isnull=True
            ).exists():
                raise ValidationError(
                    "You can't add another downtime for this device, this device is already in downtime!"
                )

        # Calculate duration whenever finish is set
        if self.start and self.finish:
            self.duration = self.finish - self.start
        else:
            self.duration = None

        super().save(*args, **kwargs)

