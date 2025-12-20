# drf:
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models:
from apps.thresholds.models import Threshold, Alert

# permissions:


# Serializers:
from apps.thresholds.serializers import ThresholdCreateSerializer, ThresholdUpdateSerializer, \
    ThresholdListSerializer, ThresholdDetailSerializer

from apps.thresholds.serializers import AlertCreateSerializer, AlertUpdateSerializer, AlertListSerializer, AlertDetailSerializer, \
        AlertFilterSerializer



from django.utils.decorators import method_decorator

# Create your views here.


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdCreateAPIView(CreateAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdCreateSerializer


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Thresholds']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdUpdateAPIView(UpdateAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'threshold_id'


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdDetailAPIView(RetrieveAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'threshold_id'


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdListAPIView(ListAPIView):
    queryset = Threshold.objects.all()
    serializer_class = ThresholdListSerializer


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdDeleteAPIView(DestroyAPIView):
    queryset = Threshold.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'threshold_id'

#==========================================================================================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Alerts']))
class AlertCreateAPIView(CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertCreateSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Alerts']))
class AlertDetailAPIView(RetrieveAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'alert_id'



from apps.thresholds.queries.alert_filter import alert_filter 
class AlertListAPIView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertListSerializer

    @swagger_auto_schema(
        tags=["Alerts"],
        manual_parameters=[
            openapi.Parameter(
                name="device_ids",
                in_=openapi.IN_QUERY,
                description="Comma-separated device IDs. Example: 1,2,3",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="device_type_ids",
                in_=openapi.IN_QUERY,
                description="Comma-separated device type IDs. Example: 4,5",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="threshold_ids",
                in_=openapi.IN_QUERY,
                description="Comma-separated threshold IDs. Example: 7,8",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="situations",
                in_=openapi.IN_QUERY,
                description="Comma-separated situations. Example: warning,critical",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                description="Start date (ISO8601)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                description="End date (ISO8601)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="order_by",
                in_=openapi.IN_QUERY,
                description="Order by field. Example: -created_at",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                description="Search in alert message",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                description="Number of records per page",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
    )    
    def get(self, request, *args, **kwargs):
        # Parse query params → dict
        params = {
            "device_ids": request.query_params.get("device_ids"),
            "device_type_ids": request.query_params.get("device_type_ids"),
            "threshold_ids": request.query_params.get("threshold_ids"),
            "situations": request.query_params.get("situations"),
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
            "order_by": request.query_params.get("order_by"),
            "search": request.query_params.get("search"),
        }

        # Convert CSV → list
        for key in ["device_ids", "device_type_ids", "threshold_ids", "situations"]:
            if params[key]:
                params[key] = params[key].split(",")

        alerts = alert_filter(params, self.get_queryset())

        page = self.paginate_queryset(alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Alerts']))
class AlertDeleteAPIView(DestroyAPIView):
    queryset = Alert.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'alert_id'










