import datetime

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from tasks.models import Task

BASE_TASK_URL = '/api/tasks/'
BASE_USER_URL = '/api/users/'


class UsersViewSetTest(APITestCase):
    def setUp(self):
        self.employee = User.objects.create(username='user', email='email@gmail.com', password='test')
        self.employee_2 = User.objects.create(username='user2', email='email2@gmail.com', password='test2')
        self.client.force_login(self.employee)

    def test_anyone_can_create_user(self):
        user_count = User.objects.count()
        self.client.post(BASE_USER_URL, {'username': 'username', 'password': 'password', 'email': 'okasdo@aokds.com'})
        self.assertEqual(user_count + 1, User.objects.count())
    #

    def test_user_cant_list_users(self):
        res = self.client.get(BASE_USER_URL)
        self.assertEqual(res.data.get('detail').code, 'permission_denied')

    def test_user_can_edit_himself(self):
        url = BASE_USER_URL + str(self.employee.id) + '/'
        self.client.put(url,
                        {'username': 'username_changed', 'password': 'password_changed', 'email': 'email@changed.com'})
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.username, 'username_changed')
        self.assertEqual(self.employee.email, 'email@changed.com')

    def test_user_cant_edit_someone_else(self):
        url = BASE_USER_URL + str(self.employee_2.id) + '/'
        res = self.client.put(url,
                        {'username': 'username_changed', 'password': 'password_changed', 'email': 'email@changed.com'})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)


class TasksViewSetTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        self.employee = User.objects.create(username='user', email='email@gmail.com', password='test')
        self.employee_2 = User.objects.create(username='user2', email='email@gmail.com', password='test')
        self.employee_hyperlink = reverse('user-list') + str(self.employee.id) + '/'
        self.client.force_login(self.superuser)
        for task in range(3):
            Task.objects.create(
                assigned_user=self.employee, title='zadanie', description='opis', deadline=datetime.datetime.now())
            Task.objects.create(
                assigned_user=self.employee_2, title='zadanie', description='opis', deadline=datetime.datetime.now())

    def test_superuser_can_create_tasks(self):
        task_count = Task.objects.count()
        self.client.post(BASE_TASK_URL,
                         {
                             'assigned_user': self.employee_hyperlink,
                             'title': 'zadanie',
                             'description': 'zadanie do wykonania',
                             'deadline': datetime.datetime.now()}
                         )
        self.assertEqual(task_count + 1, Task.objects.count())

    def test_employee_cant_create_tasks(self):
        self.client.force_login(self.employee)
        task_count = Task.objects.count()
        self.client.post(BASE_TASK_URL,
                         {
                             'assigned_user': self.employee_hyperlink,
                             'title': 'zadanie',
                             'description': 'zadanie do wykonania',
                             'deadline': datetime.datetime.now()}
                         )
        self.assertEqual(Task.objects.count(), task_count)

    #
    def test_superuser_can_edit_tasks(self):
        task = Task.objects.first()
        res = self.client.patch(BASE_TASK_URL + str(task.id) + '/',
                                {
                              'description': 'zaktualizowane'
                          })
        task.refresh_from_db()
        self.assertEqual(task.description, 'zaktualizowane')

    def test_employee_can_only_edit_status(self):
        self.client.force_login(self.employee)
        task = Task.objects.first()
        self.client.put(BASE_TASK_URL + str(task.id) + '/',
                        {
                              'description': 'zaktualizowane'
                          })
        task.refresh_from_db()
        self.assertNotEqual(task.description, 'zaktualizowane')

        self.client.put(BASE_TASK_URL + str(task.id) + '/',
                        {
                              'state': 'DONE'
                          })
        task.refresh_from_db()
        self.assertEqual(task.state, 'DONE')

    def test_employee_lists_his_tasks_only(self):
        self.client.force_login(self.employee)
        tasks_count = Task.objects.filter(assigned_user=self.employee).count()
        res = self.client.get(BASE_TASK_URL)
        self.assertEqual(tasks_count, len(res.data))

    def test_superuser_can_go_to_employees_tasks(self):
        res = self.client.get('/api/users/' + str(self.employee.id) + '/')
        print(res.data)
        tasks_url = res.data.get('tasks')
        print(tasks_url)
        res = self.client.get(tasks_url)
        tasks_count = Task.objects.filter(assigned_user=self.employee).count()
        self.assertEqual(tasks_count, len(res.data))
