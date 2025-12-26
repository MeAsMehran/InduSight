from django.db.models import Avg, Max, Min
from django.http import HttpResponse
from django.db.models.query import QuerySet
import csv

from apps.devices.services.device_status_service import device_status


def export_device_logs_to_csv(data):
    """
    data can be:
    - QuerySet (no pagination)
    - list of DeviceLog (paginated)
    """

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="device_logs_report.csv"'

    writer = csv.writer(response)

    # ================================
    # DEVICE STATUS
    # ================================
    status = device_status()
    writer.writerow(["DEVICE STATUS"])
    writer.writerow(["Online Devices", status.get("online", 0)])
    writer.writerow(["Offline Devices", status.get("offline", 0)])
    writer.writerow([])

    # ================================
    # STATS (ONLY IF QuerySet)
    # ================================
    if isinstance(data, QuerySet):
        stats = (
            data
            .values("device_type__parameter")
            .annotate(
                avg_value=Avg("value"),
                max_value=Max("value"),
                min_value=Min("value"),
            )
        )
    else:
        # Paginated list → compute stats in Python
        stats_map = {}
        for log in data:
            key = log.device_type.parameter
            stats_map.setdefault(key, []).append(log.value)

        stats = [
            {
                "device_type__parameter": k,
                "avg_value": sum(v) / len(v),
                "max_value": max(v),
                "min_value": min(v),
            }
            for k, v in stats_map.items()
        ]

    writer.writerow(["DEVICE TYPE STATISTICS"])
    writer.writerow(["Device Type", "Average Value", "Max Value", "Min Value"])

    for stat in stats:
        writer.writerow([
            stat["device_type__parameter"],
            round(stat["avg_value"], 3),
            stat["max_value"],
            stat["min_value"],
        ])

    writer.writerow([])

    # ================================
    # DEVICE LOGS
    # ================================
    writer.writerow(["DEVICE LOGS"])
    writer.writerow([
        "Device ID",
        "Device Name",
        "Device Type",
        "Time",
        "Value",
    ])

    logs = data if isinstance(data, list) else data.select_related("device", "device_type")

    for log in logs:
        writer.writerow([
            log.device.id,
            log.device.name,
            log.device_type.parameter,
            log.time.isoformat(),
            log.value,
        ])

    return response
