from rest_framework.permissions import BasePermission


class IsSupervisorUser(BasePermission):
    """
        Allows the Supervisor User to have access
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role and request.user.role.name == 'supervisor')
