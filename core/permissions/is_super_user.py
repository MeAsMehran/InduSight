from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
        Allows the Super User to have access
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser()




