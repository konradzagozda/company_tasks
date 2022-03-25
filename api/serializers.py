from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from tasks.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['url', 'assigned_user', 'title', 'description', 'state', 'deadline']


class TaskCheckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['url', 'assigned_user', 'title', 'description', 'state', 'deadline']
        read_only_fields = ['url', 'assigned_user', 'title', 'description', 'deadline']


class TaskCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['url', 'assigned_user', 'title', 'description', 'deadline']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    undone_tasks_no = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups', 'undone_tasks_no', 'tasks']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    def get_undone_tasks_no(self, obj):
        return Task.objects.filter(assigned_user=obj).count()

    def get_tasks(self, obj):
        url = reverse('task-list', request=self.context['request'])
        url += f'?assigned_user={obj.id}'
        return url


