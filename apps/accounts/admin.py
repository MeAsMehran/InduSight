from django.contrib import admin
from .models import CustomUser, Role

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'name', 'role', 'is_staff', 'is_active', 'date_joined')
    

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )
