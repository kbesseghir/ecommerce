from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedPermission(BasePermission):
    message = 'You must be authenticated to perform this action.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin to perform unsafe actions (create, update, delete).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff