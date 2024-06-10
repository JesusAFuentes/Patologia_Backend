from rest_framework.permissions import BasePermission
from apps.user.models import User


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.user_type == User.Type.ADMIN)


class IsSecretary(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.user_type == User.Type.DEPENDENCY)
