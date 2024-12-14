from rest_framework import permissions

class CanDeleteOnlySelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj