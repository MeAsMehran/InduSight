from django.urls import path
from apps.thresholds.views import ThresholdCreateAPIView, ThresholdUpdateAPIView, ThresholdDetailAPIView, \
        ThresholdListAPIView, ThresholdDeleteAPIView, AlertCreateAPIView, \
        AlertDetailAPIView, AlertListAPIView

app_name='threshold'

urlpatterns = [

    # Threshold api:
    path('threshold/create/', ThresholdCreateAPIView.as_view(), name='create_threshold'),
    path('threshold/update/<int:threshold_id>/', ThresholdUpdateAPIView.as_view(), name='update_threshold'),
    path('threshold/retrieve/<int:threshold_id>/', ThresholdDetailAPIView.as_view(), name='detail_threshold'),
    path('threshold/list/', ThresholdListAPIView.as_view(), name='list_threshold'),
    path('threshold/delete/<int:threshold_id>/', ThresholdDeleteAPIView.as_view(), name='delete_threshold'),

    # Alert api:
    path('alert/create/', AlertCreateAPIView.as_view(), name='create_alert'),
    path('alert/list/', AlertListAPIView.as_view(), name='list_alert'),
    # path('alert/delete/<int:alert_id>/', AlertDeleteAPIView.as_view(), name='delete_alert'),
    path('alert/retrieve/<int:alert_id>/', AlertDetailAPIView.as_view(), name='detail_alert'),

]


