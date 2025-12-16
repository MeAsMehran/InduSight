from django.urls import reverse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer
from django.core.cache import cache
# from .service import DeviceService
from .models import Device
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


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
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(tags=['DeviceLogs'])
)
class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
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
    serializer_class = DeviceLogSerializer


@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(tags=['DeviceLogs'])
)
class DeleteDeviceLog(DestroyAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'



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


