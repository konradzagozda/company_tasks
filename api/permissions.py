from rest_framework import permissions


class UsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        # allow anyone to create users
        if view.action == 'create':
            return True
        # specified in has_object_permission what to do depending on what object it is
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action == 'retrieve':
            return obj == request.user or request.user.is_superuser
        if view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_superuser
        if view.action == 'destroy':
            return request.user.is_superuser
        return False


class TasksPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            if view.action in ['retrieve', 'update', 'partial_update', 'list']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action == 'retrieve':
            return obj.assigned_user == request.user or request.user.is_superuser
        if view.action in ['update', 'partial_update']:
            return obj.assigned_user == request.user or request.user.is_superuser
        if view.action == 'destroy':
            return request.user.is_superuser
        return False
