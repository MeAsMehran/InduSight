from django.urls import path
from apps.thresholds.views import ThresholdCreateAPIView, ThresholdUpdateAPIView, ThresholdDetailAPIView, \
        ThresholdListAPIView, ThresholdDeleteAPIView

app_name='threshold'

urlpatterns = [

    # Threshold api:
    path('threshold/create/', ThresholdCreateAPIView.as_view(), name='create_threshold'),
    path('threshold/update/<int:threshold_id>/', ThresholdUpdateAPIView.as_view(), name='update_threshold'),
    path('threshold/retrieve/<int:threshold_id>/', ThresholdDetailAPIView.as_view(), name='detail_threshold'),
    path('threshold/list/', ThresholdListAPIView.as_view(), name='list_threshold'),
    path('threshold/delete/<int:threshold_id>/', ThresholdDeleteAPIView.as_view(), name='delete_threshold'),

    # Alert api:
    # path('alert/create/', CreateDeviceType.as_view(), name='create_device_type'),
    # path('alert/list/', ListDeviceType.as_view(), name='list_device_type'),
    # path('alert/delete/<int:id>/', DeleteDeviceType.as_view(), name='delete_device_type'),
    # path('alert/retrieve/<int:id>/', DetailDeviceType.as_view(), name='detail_device_type'),


]


