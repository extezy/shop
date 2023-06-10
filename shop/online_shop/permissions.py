from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and
             (request.user.is_staff or request.user.is_superuser))
        )
