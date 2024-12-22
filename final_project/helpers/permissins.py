from rest_framework import permissions


class CanDeleteOnlySelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
