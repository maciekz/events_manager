from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Permission is granted only to the creator of the event.
        return obj.creator == request.user
