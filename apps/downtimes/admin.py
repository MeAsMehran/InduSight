from django.contrib import admin
from apps.downtimes.models import Downtime  

# Register your models here.

@admin.register(Downtime)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'start', 'finish', 'reason',)
    search_fields = ('device', 'reason')
    

