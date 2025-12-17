from django.db.models import Q
from django.utils import timezone
from apps.devices.models import Device, DeviceType, DeviceLog


def dev_log_filter(params, device_logs):

    start_date = params.get('start_date')
    end_date = params.get('end_date')
    device_ids = params.get('device_ids')
    device_type_ids = params.get('device_type_ids')
    order_by = params.get('order_by')
    latest = params.get('latest')
    search = params.get('search')



    our_filter = Q()

    # Date:
    # if start_date and not end_date:
    #     our_filter = our_filter & Q(time__gte=start_date) & Q(time__lte=timezone.now())
    #
    # if not start_date and end_date:
    #     our_filter = our_filter & Q(time__lte=end_date)

    # if start_date and end_date:
    #     our_filter = our_filter & Q(time__range=(start_date, end_date))
    #
    # # device ids and device type ids:
    # if device_ids:
    #     our_filter = our_filter & Q(device_id__in=device_ids)
    #
    # if device_type_ids:
    #     our_filter = our_filter & Q(device_type_id__in=device_type_ids)
    #
    # # searching:
    # if search:
    #     our_filter = our_filter & (Q(device__name__icontains=search) |
    #                                Q(device_type__parameter__icontains=search))

    
    filtered_device_logs = device_logs.filter(
        Q(time__range=(start_date, end_date)) & 
        Q(device_id__in=device_ids) &
        ((device_type_ids and Q(device_type_id__in=device_type_ids)) or Q()) &
        ((search and (
            Q(device__name__icontains=search) |
            Q(device_type__parameter__icontains=search)
        )) or Q())
    ).order_by(
        *((order_by and (f"{order_by}",)) or ())
    )

    # filtered_device_logs = device_logs.filter(our_filter)
    
    # ordering:
    # if order_by:
    #     if latest:
    #         filtered_device_logs = filtered_device_logs.order_by(f"-{order_by}")
    #     else:
    #         filtered_device_logs = filtered_device_logs.order_by(order_by)
    #
    return filtered_device_logs


