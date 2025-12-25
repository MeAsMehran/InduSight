from rest_framework.permissions import BasePermission
from apps.devices.models import Device


class IsSupervisorUser(BasePermission):
    """
        Allows the Supervisor User to have access
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role and request.user.role.name == 'supervisor')


class IsSupervisorAndDeviceOwner(BasePermission):
    """
        Allows the supervisor User to have access to only his/her devices.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role.name == "supervisor" and
            obj.supervisor.filter(pk=request.user.pk).exists())     # obj.supervisor is queryset

        # return (
        #             request.user.is_authenticated
        #             and request.user.role.name == "supervisor"
        #             and request.user in obj.supervisor.all()
        #         )
        

class IsSupervisorOfDevice(BasePermission):
    """
    Allows supervisors to manage thresholds only for devices they supervise.
    """

    def has_permission(self, request, view):
        # Authentication required
        if not request.user or not request.user.is_authenticated:
            return False

        # CREATE: check device from request data
        if request.method == "POST":
            device_id = request.data.get("device")
            if not device_id:
                return False

            try:
                device = Device.objects.get(pk=device_id)
            except Device.DoesNotExist:
                return False

            return device.supervisor.filter(pk=request.user.pk).exists()

        return True

    def has_object_permission(self, request, view, obj):
        # DELETE / UPDATE / RETRIEVE
        # obj is a Threshold instance
        return obj.device.supervisor.filter(pk=request.user.pk).exists()


class IsAdminOrDeviceSupervisor(BasePermission):
    """
    Admins can access all devices.
    Supervisors can access only devices they supervise.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Supervisor owns device (ManyToMany)
        return obj.supervisor.filter(pk=request.user.pk).exists()
