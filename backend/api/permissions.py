from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class CurrentUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user == obj or request.user.is_superuser
            )
        )
