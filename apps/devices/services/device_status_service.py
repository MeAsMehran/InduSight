from apps.devices.models import Device, DeviceType, DeviceLog
from django.utils import timezone
from django.core.cache import caches

def device_status():
    now = timezone.now()
    online_count = 0
    offline_count = 0
    cache = caches['default']

    devices = Device.objects.all()

    for device in devices:
        cache_key = f"device:{device.id}:status"
        status = cache.get(cache_key)

        if status is None:
            last_log = DeviceLog.objects.filter(device=device).order_by('-time').first()

            if not last_log:
                status = "Offline"
            else:
                time_difference = (now - last_log.time).total_seconds()
                status = "Online" if time_difference <= 120 else "Offline"

            cache.set(cache_key, status, timeout=30)

        if status == "Online":
            online_count += 1
        else:
            offline_count += 1

    return {
        "online": online_count,
        "offline": offline_count
    }

