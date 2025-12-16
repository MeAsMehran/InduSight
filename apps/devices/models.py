from django.db import models

# Create your models here.


class DeviceType(models.Model):

    # device = models.ForeignKey(Device, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=100, )
    code = models.CharField(unique=True)
    des = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.parameter}"


class Device(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(unique=True)
    des = models.CharField(max_length=250, blank=True, null=True)
    device_type = models.ManyToManyField(DeviceType,)

    def __str__(self) -> str:
        return str(self.name)


class DeviceLog(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(default=0)


# class Stop(models.Model):
#
#     device = models.ForeignKey(Device, on_delete=models.CASCADE)
#     start = models.DateTimeField(auto_now_add=True)
#     end = models.DateTimeField()
