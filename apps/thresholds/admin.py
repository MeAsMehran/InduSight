from django.contrib import admin
from apps.thresholds.models import Threshold, Alert 

# Register your models here.

@admin.register(Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'device_type', 'min_value', 'max_value', 'active')
    search_fields = ('device', 'device_type')
    
    
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'device_type', 'threshold', 'value', 'situation', 'message', 'created_at')
    search_fields = ('message', 'threshold')
    ordering = ('-created_at',)


