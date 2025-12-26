from rest_framework import serializers
from apps.thresholds.models import Threshold, Alert
from django.utils import timezone
from apps.devices.models import Device
from django.shortcuts import get_object_or_404



# serializer classes:

class ThresholdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = '__all__'

    def validate(self, attrs):
        instance = Threshold(**attrs)   # create an instance from Threshold with the attrs
        instance.full_clean()   # check the attrs values with full_clean() which validate the the condition we set for saving a Threshold object in db!
        return attrs


class ThresholdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = '__all__'


class ThresholdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = '__all__'


class ThresholdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = '__all__'

# ===================================================================================================================

class AlertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

    def validate(self, attrs):
        # run model-level validation
        instance = Alert(**attrs)   # create an instance from Threshold with the attrs
        instance.full_clean()   # check the attrs values with full_clean() which validate the the condition we set for saving a Threshold object in db! 
        return attrs


class AlertUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class AlertDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class AlertListSerializer(serializers.ModelSerializer):
    
    device_name = serializers.CharField(source='device.name', read_only=True)
    device_type_name = serializers.CharField(source='device_type.name', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id',
            'device',
            'device_name',
            'device_type',
            'device_type_name',
            'threshold',
            'value',
            'situation',
            'message',
            'created_at',
            'is_above_max',
            'is_below_min',
        ]
        read_only_fields = ['created_at']
    

# class AlertFilterSerializer(serializers.Serializer):
#
#     device_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         required=False,
#         allow_empty=False
#     )
#
#     device_type_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         required=False,
#         allow_empty=False
#     )
#
#     threshold_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         required=False,
#         allow_empty=False
#     )
#
#     situations = serializers.ListField(
#         child=serializers.CharField(),
#         required=False,
#         allow_empty=False
#     )
#
#     start_date = serializers.DateTimeField(required=False, allow_null=True)
#     end_date = serializers.DateTimeField(required=False, allow_null=True)
#
#     search = serializers.CharField(required=False, allow_null=True)
#     order_by = serializers.CharField(required=False, allow_null=True)
#
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#     page_number = serializers.IntegerField(required=False, allow_null=True)
#
#     def validate(self, attrs):
#         start = attrs.get("start_date")
#         end = attrs.get("end_date")
#
#         if start and end and start > end:
#             raise serializers.ValidationError(
#                 "start_date must be earlier than end_date"
#             )
#
#         return attrs


