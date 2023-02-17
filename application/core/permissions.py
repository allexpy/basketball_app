from rest_framework import permissions

from accounts.models import CustomUser


class AdminsOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type == CustomUser.UserTypes.ADMIN:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.type == CustomUser.UserTypes.ADMIN:
            return True
        return False


class UsersOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type == CustomUser.UserTypes.NORMAL:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.type == CustomUser.UserTypes.NORMAL:
            return True
        return False
