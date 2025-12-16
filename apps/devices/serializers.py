from rest_framework import serializers
from .models import Device, DeviceLog, DeviceType
from django.utils import timezone



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

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        device_type_ids = validated_data.pop('device_type_ids', [])
        device = Device.objects.create(**validated_data)
        device.device_type.set(device_type_ids)
        return device


class DeviceLogSerializer(serializers.Serializer):

    device_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=True,
        required=False
    )
    device_type_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        required=False
    )
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        fields = ('device_ids', 'device_type_ids', 'start_date', 'end_date')


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

    class Meta:
        fields = ('id', 'device', 'device_type', 'time', 'value')


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


