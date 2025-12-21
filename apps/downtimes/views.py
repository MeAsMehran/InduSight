from apps.downtimes.serializers import DowntimeSerializer
from rest_framework.views import APIView
from apps.devices.models import Device
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from apps.downtimes.models import Downtime
from rest_framework.exceptions import ValidationError

# Create your views here.


class DowntimeAPIView(APIView):

    @swagger_auto_schema(request_body=DowntimeSerializer)
    def post(self, request):
        # First validation:
        serializer = DowntimeSerializer(data=request.data)
        
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        # Extract the serializers fields:
        device = serializer.validated_data['device']
        time = serializer.validated_data['time']
        
        # Check if the device is already in downtime or not:
        if Downtime.objects.filter(device=device, finish__isnull=True).exists():
            active_downtime = Downtime.objects.filter(device=device, finish__isnull=True).first()
                
            # CASE 1: Finish existing downtime
            if active_downtime:
                if time < active_downtime.start:
                    raise ValidationError(
                        {"time": "Finish time cannot be earlier than start time."}
                    )

                active_downtime.finish = time
                active_downtime.save()

                return Response(
                    {
                        "device": active_downtime.device.id,
                        "start": active_downtime.start,
                        "finish": active_downtime.finish,
                        "duration": active_downtime.duration,
                        "reason": active_downtime.reason,
                    },
                    status=status.HTTP_200_OK
                )

        # CASE 2: Start downtime
        downtime = Downtime.objects.create(
            device=device,
            start=time,
            reason=serializer.validated_data.get('reason')
        )

        return Response(
            {
                "device": downtime.device.id,
                "start": downtime.start,
                "finish": downtime.finish,
                "duration": downtime.duration,
                "reason": downtime.reason,
            },
            status=status.HTTP_201_CREATED
        )
