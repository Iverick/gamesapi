# rest_framework import
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Allows GET, HEAD and OPTIONS requests to the object for non owner users.

    Sets an owner value to an user object if owner field hasn't been assigned
        to nobody yet.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user
