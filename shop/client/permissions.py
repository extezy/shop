from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            (request.user and
             (request.user.is_staff or request.user.is_superuser)
             )
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and (
                request.user and
                (request.user.is_staff or request.user.is_superuser)
        ):
            return True

        return obj.user == request.user
