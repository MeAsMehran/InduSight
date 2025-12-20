from django.db import models
from apps.devices.models import Device

# Create your models here.

REASON = (
    ('periodic_maintenance', 'Periodic Maintenance'),
    ('hardware_failure', 'Hardware Failure'),
    ('system_update', 'System Update'),
)

class Downtime(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='downtimes') 
    start = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField(null=True) 
    reason = models.CharField(max_length=512, choices=REASON, blank=False, null=False)

    def __str__(self):
        return self.device.name
