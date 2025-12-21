from django.urls import path
from apps.downtimes.views import DowntimeAPIView


app_name='downtime'

urlpatterns = [

    # Device api:
    path('downtime/check/', DowntimeAPIView.as_view(), name='downtime_check'),
    # path('downtime/finish/<int:id>/', DowntimeFinishAPIView.as_view(), name='finish_downtime'),
    # path('downtime/list/', DowntimeListAPIView.as_view(), name='list_downtime'),

]
