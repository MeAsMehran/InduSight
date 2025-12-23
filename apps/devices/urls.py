from django.urls import path
from apps.devices.views import CreateDevice, DetailDevice, ListDevice, \
    DeleteDevice, CreateDeviceType, ListDeviceType, DeleteDeviceType, DetailDeviceType, CreateDeviceLog, \
    DetailDeviceLog, ListDeviceLog, DeleteDeviceLog, UpdateDeviceStatusAPIView, GetDeviceStatusReportAPIView \

app_name='machine'

urlpatterns = [

    # Device api:
    path('device/create/', CreateDevice.as_view(), name='create_device'),
    path('device/retrieve/<int:id>/', DetailDevice.as_view(), name='detail_device'),
    path('device/list/', ListDevice.as_view(), name='list_device'),
    path('device/delete/<int:id>/', DeleteDevice.as_view(), name='delete_device'),

    # DeviceType api:
    path('device_type/create/', CreateDeviceType.as_view(), name='create_device_type'),
    path('device_type/list/', ListDeviceType.as_view(), name='list_device_type'),
    path('device_type/delete/<int:id>/', DeleteDeviceType.as_view(), name='delete_device_type'),
    path('device_type/retrieve/<int:id>/', DetailDeviceType.as_view(), name='detail_device_type'),

    # DeviceLog api:
    path('device_log/create/', CreateDeviceLog.as_view(), name='create_device_log'),
    path('device_log/retrieve/<int:id>/', DetailDeviceLog.as_view(), name='detail_device_log'),
    path('device_log/list/', ListDeviceLog.as_view(), name='list_device_log'),
    path('device_log/delete/<int:id>/', DeleteDeviceLog.as_view(), name='delete_device_log'),
    path('device_log/reports/overview/', GetDeviceStatusReportAPIView.as_view(), name='device_log_reports'),

    # Device Status:
    path('device/<int:device_id>/status/', UpdateDeviceStatusAPIView.as_view(), name='device_status'),

]
