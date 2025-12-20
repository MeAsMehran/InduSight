from django.urls import path
from apps.devices.views import CreateDevice, SendDate, ReceivedData, DetailDevice, ListDevice, \
    DeleteDevice, CreateDeviceType, ListDeviceType, DeleteDeviceType, DetailDeviceType, CreateDeviceLog, \
    DetailDeviceLog, ListDeviceLog, DeleteDeviceLog, UpdateDeviceStatusAPIView, GetDeviceStatusReportAPIView \

app_name='downtime'

urlpatterns = [

    # Device api:
    path('downtime/start/', CreateDevice.as_view(), name='create_device'),
    path('downtime/finish/<int:id>/', DetailDevice.as_view(), name='detail_device'),
    path('device/list/', ListDevice.as_view(), name='list_device'),

]
