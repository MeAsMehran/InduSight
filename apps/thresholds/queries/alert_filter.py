from django.db.models import Q

def alert_filter(params, alerts):

    start_date = params.get("start_date")
    end_date = params.get("end_date")
    device_ids = params.get("device_ids")
    device_type_ids = params.get("device_type_ids")
    threshold_ids = params.get("threshold_ids")
    situations = params.get("situations")
    search = params.get("search")
    order_by = params.get("order_by")

    filtered_alerts = alerts.filter(
        # date range
        ((start_date and end_date and Q(created_at__range=(start_date, end_date))) or Q()) &
        ((start_date and not end_date and Q(created_at__gte=start_date)) or Q()) &
        ((end_date and not start_date and Q(created_at__lte=end_date)) or Q()) &

        # device
        ((device_ids and Q(device_id__in=device_ids)) or Q()) &

        # device type
        ((device_type_ids and Q(device_type_id__in=device_type_ids)) or Q()) &

        # threshold
        ((threshold_ids and Q(threshold_id__in=threshold_ids)) or Q()) &

        # situation
        ((situations and Q(situation__in=situations)) or Q()) &

        # search
        ((search and Q(message__icontains=search)) or Q())
    ).order_by(
        *((order_by and (order_by,)) or ())
    )

    return filtered_alerts
