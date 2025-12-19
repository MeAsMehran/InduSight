from rest_framework import serializers
from apps.thresholds.models import Threshold, Alert
from django.utils import timezone


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
        instance = Alert(**attrs)
        instance.full_clean()
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
    class Meta:
        model = Alert
        fields = '__all__'


