from rest_framework import permissions


class IsAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
