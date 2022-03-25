from django.contrib.auth.models import User
from rest_framework import viewsets

from api.permissions import UsersPermission, TasksPermission
from tasks.models import Task
from api.serializers import TaskSerializer, UserSerializer, TaskCheckSerializer, TaskCreateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TasksPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_superuser:
            if self.action == 'create':
                serializer_class = TaskCreateSerializer
            return serializer_class
        if self.request.method in ['PUT', 'POST']:
            serializer_class = TaskCheckSerializer
        return serializer_class

    def get_queryset(self):
        queryset = Task.objects.all()
        if self.request.user.is_superuser:
            assigned_user = self.request.query_params.get('assigned_user')
            if assigned_user:
                return queryset.filter(assigned_user=assigned_user)
            return queryset
        else:
            user = self.request.user
            return queryset.filter(assigned_user=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UsersPermission]
