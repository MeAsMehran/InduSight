from rest_framework import serializers
from .models import Device, DeviceLog, DeviceType
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.thresholds.models import Threshold, Alert
from rest_framework.exceptions import ValidationError



class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    device_type = serializers.StringRelatedField(many=True, read_only=True)

    device_type_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DeviceType.objects.all(),
        write_only=True
    )

    supervisor = serializers.StringRelatedField(many=True, read_only=True)

    supervisor_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all(),
        write_only=True
    )

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        supervisors = validated_data.pop('supervisor_ids', [])
        device_type_ids = validated_data.pop('device_type_ids', [])

        device = Device.objects.create(**validated_data)

        device.device_type.set(device_type_ids)
        device.supervisor.set(supervisors)

        return device

from apps.devices.tasks import alert_send_mail
from apps.devices.validations.device_log_validate import device_log_validate
class DeviceLogCreateSerializer(serializers.ModelSerializer):
    device = serializers.CharField()
    device_type = serializers.CharField()

    class Meta:
        model = DeviceLog
        fields = ('device', 'device_type', 'value')

    def validate(self, attrs):
        return device_log_validate(data=attrs)

    def create(self, validated_data):
        # request = self.context.get("request")
        #
        # if request is not None:
        #     user = request.user
        # else:
        #     user = None

        device = validated_data.get('device')
        device_type = validated_data.get('device_type')
        value = validated_data.get('value')

        # Get the device threshold:
        try:
            threshold = Threshold.objects.get(device=device, device_type=device_type)
        except Threshold.DoesNotExist:
            raise ValidationError("No Threshold found!")

        # if device threshold was active:
        if threshold.active:
            if value > threshold.max_value:
                alert = Alert.objects.create(
                        device=device,
                        device_type=device_type,
                        threshold=threshold,
                        value=value,
                        situation="above_max",
                        message=f"The value:{value} of device_type:{device_type} from device:{device} with code:{device.code} is above its threshold:{threshold.max_value}")

                print(
                    "\033[91m"              # red
                    "\n⚠️ ALARM ⚠️\n"
                    f"[ALERT] device={device.code}\n"
                    f"type={device_type}\n"
                    f"value={value}\n"
                    f"max={threshold.max_value}\n"
                    "situation=above_max\n"
                    "\033[0m"               # reset color
                )
                    # alert_send_mail.delay(user_email=user.email, alert_message=alert.message)
                alert_send_mail.delay(alert_message=alert.message)

            elif value < threshold.min_value:
                alert = Alert.objects.create(
                        device=device,
                        device_type=device_type,
                        threshold=threshold,
                        value=value,
                        situation="below_min",
                        message=f"The value:{value} of device_type:{device_type} with code:{device_type.code} from device:{device} with code:{device.code} is below its threshold:{threshold.min_value}")
                
                print(
                    "\033[91m"              # red
                    "\n⚠️ ALARM ⚠️\n"
                    f"[ALERT] device={device.code}\n"
                    f"type={device_type}\n"
                    f"value={value}\n"
                    f"min={threshold.min_value}\n"
                    "situation=below_min\n"
                    "\033[0m"               # reset color
                )
                # alert_send_mail.delay(user_email=user.email, alert_message=alert.message)
                alert_send_mail.delay(alert_message=alert.message)


        return super().create(validated_data)


class DeviceLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DeviceLog
        fields = "__all__"


from apps.devices.validations.params_validate import params_validate
class DeviceLogListSerializer(serializers.Serializer):

    device_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        required=True,
    )
    device_type_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        required=False
    )

    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)

    order_by = serializers.CharField(required=False, allow_null=True)
    search = serializers.CharField(required=False, allow_null=True)

    page_size = serializers.IntegerField(required=False, allow_null=True)
    page_number = serializers.IntegerField(required=False, allow_null=True)

    export = serializers.ChoiceField(choices=["csv"], required=False, allow_null=True)

    class Meta:
        model = DeviceLog
        fields = ('device_ids', 'device_type_ids', 'page_size', 'page_number','order_by','search','start_date', 'end_date', 'export')

    def validate(self, attrs):
        return params_validate(data=attrs)


class DeviceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name')


class DeviceTypeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'parameter')


class DeviceLogOutputSerializer(serializers.Serializer):

    device = DeviceNestedSerializer()
    device_type = DeviceTypeNestedSerializer()
    time = serializers.DateTimeField()
    value = serializers.FloatField()
    supervisor = serializers.SerializerMethodField(read_only=True)  # This is for the test 

    class Meta:
        fields = ('id', 'device', 'device_type', 'time', 'value')

    def get_supervisor(self, obj):
        return [
            user.role.name
            for user in obj.device.supervisor.all()
            if user.role
        ]


class DeviceLogStatsSerializer(serializers.Serializer):
    # device_type_id = serializers.IntegerField(source="device_type__id")
    device_type = serializers.CharField(source="device_type__parameter")
    avg_value = serializers.FloatField()
    max_value = serializers.FloatField()
    min_value = serializers.FloatField()


# For PUT request method
class DeviceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceTypeUpdateSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = DeviceType
            fields = ('parameter', 'code', 'des')


class DeviceTypeOutputSerializer(serializers.Serializer):

    class Meta:
        model = DeviceType
        fields = ('parameter', 'code')


class DeviceOutputSerializer(serializers.Serializer):
    device_type = DeviceTypeOutputSerializer(many=True) 

    class Meta:
        model = Device
        fields = ('code', 'name', 'device_type')


class DataSerializerSerializer(serializers.Serializer):
    machine_code = serializers.CharField()
    machine_name = serializers.CharField()
    device_type = DeviceTypeSerializer(many=True)

    class Meta:
        fields = ('machine_code', 'machine_name', 'device_type')


