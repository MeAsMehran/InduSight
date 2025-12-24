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
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_super_user import IsSuperUser
from core.permissions.is_admin_user import IsAdminUser
from core.permissions.is_supervisor_user import IsSupervisorUser, IsSupervisorOfDevice
from core.permissions.is_not_authenticated import IsNotAuthenticated

# Serializers:
from apps.thresholds.serializers import ThresholdCreateSerializer, ThresholdUpdateSerializer, \
    ThresholdListSerializer, ThresholdDetailSerializer

from apps.thresholds.serializers import AlertCreateSerializer, AlertUpdateSerializer, AlertListSerializer, AlertDetailSerializer

# Filtering -> 'django_filters':
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from django.utils.decorators import method_decorator

# Create your views here.


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    queryset = Threshold.objects.all()
    serializer_class = ThresholdCreateSerializer


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Thresholds']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    queryset = Threshold.objects.all()
    serializer_class = ThresholdUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'threshold_id'


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    queryset = Threshold.objects.all()
    serializer_class = ThresholdDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'threshold_id'


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    queryset = Threshold.objects.all()
    serializer_class = ThresholdListSerializer


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Thresholds']))
class ThresholdDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
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


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Alerts']))
class AlertListAPIView(ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter,]
    filterset_fields = ['value', 'situation', 'device']
    search_fields = ['message', 'device__name', 'device_type__parameter']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Alerts']))
class AlertDeleteAPIView(DestroyAPIView):
    queryset = Alert.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'alert_id'

