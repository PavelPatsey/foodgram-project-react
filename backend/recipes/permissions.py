from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (obj.author == request.user or request.user.is_superuser)
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
