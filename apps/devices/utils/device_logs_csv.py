
import csv
from django.http import HttpResponse
from django.db.models import Avg, Max, Min

from apps.devices.services.device_status_service import device_status


def export_device_logs_to_csv(queryset):
    """
    Export device logs with:
    - online/offline device counts
    - avg/max/min value per device type
    - raw device log rows
    """

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="device_logs_report.csv"'

    writer = csv.writer(response)

    # STATUS (ONLINE/OFFLINE DEVICES) 
    status = device_status()

    writer.writerow(["DEVICE STATUS"])
    writer.writerow(["Online Devices", status.get("online", 0)])
    writer.writerow(["Offline Devices", status.get("offline", 0)])
    writer.writerow([])

    # AVG/MIN/MAX PARAMETER VALUE:
    stats = (
        queryset
        .values("device_type__parameter")
        .annotate(
            avg_value=Avg("value"),
            max_value=Max("value"),
            min_value=Min("value"),
        )
    )

    writer.writerow(["DEVICE TYPE STATISTICS"])
    writer.writerow(["Device Type", "Average Value", "Max Value", "Min Value"])

    for stat in stats:
        writer.writerow([
            stat["device_type__parameter"],
            round(stat["avg_value"], 3) if stat["avg_value"] is not None else "",
            stat["max_value"],
            stat["min_value"],
        ])

    writer.writerow([])

    # DEVICE LOGS:
    writer.writerow(["DEVICE LOGS"])
    writer.writerow([
        "Device ID",
        "Device Name",
        "Device Type",
        "Time",
        "Value",
    ])

    for log in queryset.select_related("device", "device_type"):
        writer.writerow([
            log.device.id,
            log.device.name,
            log.device_type.parameter,
            log.time.isoformat(),
            log.value,
        ])

    return response

