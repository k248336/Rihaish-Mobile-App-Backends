from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission: only allow owners of an object to edit/delete it.
    Read access is allowed to any authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Write permissions only for the owner
        return obj.owner == request.user


class IsOwner(BasePermission):
    """
    Custom permission: only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
