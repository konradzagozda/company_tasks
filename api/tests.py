from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient


class UsersViewSetTest(APITestCase):
    BASE_URL = '/api/users/'

    def test_anyone_can_create_user(self):
        user_count = User.objects.count()
        self.client.post(self.BASE_URL, {'username': 'username', 'password': 'password', 'email': 'okasdo@aokds.com'})
        self.assertEqual(user_count + 1, User.objects.count())


class TasksViewSetTest(APITestCase):
    BASE_URL = '/api/tasks/'

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        self.employee = User.objects.create(username='user', email='email@gmail.com', password='test')