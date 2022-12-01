from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # Override the super class's has_object_permission method
    def has_object_permission(self, request, view, obj):
        # Check if user is requesting read only access
        # and if so grant access.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, test if the user is the owner of the profile
        # and return the result which determines if they get access
        return obj.owner == request.user