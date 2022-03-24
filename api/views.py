from django.contrib.auth.models import User
from rest_framework import viewsets

from api.permissions import UsersPermission, TasksPermission
from tasks.models import Task
from api.serializers import TaskSerializer, UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TasksPermission]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UsersPermission]
