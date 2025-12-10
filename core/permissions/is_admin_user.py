from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
        Allows the Admin User to have access
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role and request.user.role.name == 'admin')