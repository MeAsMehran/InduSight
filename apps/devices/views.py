from django.urls import reverse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer, DeviceLogOutputSerializer, DeviceLogCreateSerializer
from django.core.cache import caches
# from .service import DeviceService
from .models import Device
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from core.permissions.is_supervisor_user import IsSupervisorAndDeviceOwner


# from .tasks import process_receive_send_data


# Create your views here.

# DEVICE CRUD:
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(tags=['Devices'])
)
class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAdminUser]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['Devices'])
)
class ListDevice(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['Devices'])
)
class DetailDevice(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'


@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(tags=['Devices'])
)
class DeleteDevice(DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'


# DEVICE TYPE CRUD:
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(tags=['DeviceTypes'])
)
class CreateDeviceType(CreateAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['DeviceTypes'])
)
class DetailDeviceType(RetrieveAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    lookup_field = 'id'


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['DeviceTypes'])
)
class ListDeviceType(ListAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(tags=['DeviceTypes'])
)
class DeleteDeviceType(DestroyAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    lookup_field = 'id'


# DEVICE LOG CRUD:
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['DeviceLogs']))
class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogCreateSerializer
    # permission_classes = [IsAdminUser]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['DeviceLogs'])
)
class DetailDeviceLog(RetrieveAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=['DeviceLogs'])
)
class ListDeviceLog(ListAPIView):
    queryset = DeviceLog.objects.all()
    permission_classes = [IsAuthenticated & (IsAdminUser | IsSupervisorAndDeviceOwner)]
    serializer_class = DeviceLogOutputSerializer

    def get_queryset(self):
        user = self.request.user 

        if user.role.name == 'admin':
            return DeviceLog.objects.all()[0:30]

        if user.role.name == 'supervisor':
            return DeviceLog.objects.filter(device__supervisor=user)[0:30]

        return DeviceLog.objects.none()


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['DeviceLogs']))
class DeleteDeviceLog(DestroyAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Devices']))
class UpdateDeviceStatusAPIView(APIView):

    def setup(self, request, *args, **kwargs):
        self.cache = caches['default']
        return super().setup(request, *args, **kwargs)

    def post(self, request, device_id):
        last_device_log = DeviceLog.objects.filter(device=device_id).order_by('-time').first()
        device = get_object_or_404(Device, id=device_id)
        device_data_types = device.device_type.values_list('id', flat=True)     # device data types -> [1, 3, 4]
        lately_data = []
        
        if not last_device_log:
            # device is offline
            self.cache.set(f"device:{device_id}:status", "Offline", timeout=30)
            return Response({f"device:{device_id}:status" : "Offline"})

        for data_type in device_data_types:
            data_type_log = DeviceLog.objects.filter(device=device, device_type=data_type).order_by('-time').first()

            if data_type_log is not None:
                value = data_type_log.value
            else:
                value = None

            data_type_log_json = {
                    f"{DeviceType.objects.get(id=data_type).parameter}" : value
                }
            lately_data.append(data_type_log_json)


        now_time = timezone.now() 
        last_device_log_time = last_device_log.time 
        difference = (now_time - last_device_log_time).total_seconds()

        if difference <= 120:
            # device is online
            self.cache.set(f"device:{last_device_log.device.id}:status", "Online", timeout=30)
            return Response({f"device:{device_id}:status" : "Online"})
            
        else:
            # device is offline
            self.cache.set(f"device:{last_device_log.device.id}:status", "Offline", timeout=30)
            return Response({f"device:{device_id}:status" : "Offline"})


# class GetDeviceStatusAPIView(APIView):
         


        

    



class ShowDataView(APIView):
    def post(self, request, *args, **kwargs):
        # received_data = request.data  # this contains the JSON sent by DetailDevice
        # serializer = DeviceSerializer(ReceiveData)
        received_data = cache.get('cached_data')

        if received_data:
            return Response({
                "message": "Data received successfully",
                "received_data": received_data  # make sure to return the variable
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Failed Receiving data!",
                "received_data": received_data  # make sure to return the variable
            }, status=status.HTTP_404_NOT_FOUND)


# class MachineStatusView(APIView):
#
#     def get(self, request, id):
#         # machine = Device.objects.get(id=machine_id)
#         result = DeviceService.process_machine(machine_id=id)
#
#         if result is not None:
#             data = result['data']
#         else:
#             data = {'status' : "Offline", 'message': "No data received"}
#
#         url_path = reverse("machine:show_data")
#         target_url = request.build_absolute_uri(url_path)
#         requests.post(target_url, json=data)
#
#         if data:
#             return JsonResponse({
#                 "machine": Device.objects.get(pk=id).name,
#                 "status": "online",
#                 "data": data,
#             })
#
#         return JsonResponse({
#             "machine": Device.objects.get(pk=id).name,
#             "status": "offline",
#             "data": None,
#         })


class SendDate(APIView):
    permission_classes = [IsAdminUser]

    
class ReceivedData(APIView):
    permission_classes = [IsAdminUser]


