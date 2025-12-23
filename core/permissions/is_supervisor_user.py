from rest_framework.permissions import BasePermission


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
        obj.objects.get(device)
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
