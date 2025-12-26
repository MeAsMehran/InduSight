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
from core.permissions.is_supervisor_user import IsSupervisorUser, IsSupervisorOfDevice, IsAdminOrDeviceSupervisor
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

    def get_queryset(self):
        user = self.request.user

        # Admin sees everything
        if user.role.name == 'admin' or user.is_superuser:
            return Threshold.objects.all()

        # Supervisor sees only owned devices
        return Threshold.objects.filter(device__supervisor=user)
    


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
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    queryset = Alert.objects.all()
    serializer_class = AlertDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'alert_id'



value_param = openapi.Parameter(
    'value', openapi.IN_QUERY, type=openapi.TYPE_NUMBER
)

situation_param = openapi.Parameter(
    'situation', openapi.IN_QUERY, type=openapi.TYPE_STRING
)

device_param = openapi.Parameter(
    'device', openapi.IN_QUERY, type=openapi.TYPE_INTEGER
)

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Alerts'],
        manual_parameters=[value_param, situation_param, device_param],
    )
)
class AlertListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorOfDevice)]
    # queryset = Alert.objects.all()
    serializer_class = AlertListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter,]
    filterset_fields = {
            'device': ['exact', 'in'],
            'situation': ['exact'],
            'value': ['exact', 'gte', 'lte'],
            'created_at': ['gte', 'lte'],
        }
    search_fields = ['message', 'device__name', 'device_type__parameter']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user

        # Admin sees everything
        if user.role.name == 'admin' or user.is_superuser:
            return Alert.objects.all()

        # Supervisor sees only owned devices
        return Alert.objects.filter(device__supervisor=user)
    
    

# @method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Alerts']))
# class AlertDeleteAPIView(DestroyAPIView):
#     queryset = Alert.objects.all()
#     lookup_field = 'id'
#     lookup_url_kwarg = 'alert_id'

