from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser


class RecipePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        base_user_perm = not user.blocked or request.method in SAFE_METHODS
        return base_user_perm or user.is_superuser

    def has_object_permission(self, request, view, obj):
        user = request.user
        base_user_perm = not user.blocked or request.method in SAFE_METHODS
        return user.is_superuser or obj.author is user or base_user_perm
