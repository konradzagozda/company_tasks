from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from api.permissions import UsersPermission, TasksPermission
from tasks.models import Task
from api.serializers import TaskSerializer, UserSerializer, TaskCheckSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TasksPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_superuser:
            return serializer_class

        if self.request.method in ['PUT', 'POST']:
            serializer_class = TaskCheckSerializer

        return serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        else:
            user = self.request.user
            return self.queryset.filter(assigned_user=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UsersPermission]

