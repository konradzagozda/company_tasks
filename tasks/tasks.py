from celery import shared_task
from django.core.mail import send_mail

from company_tasks.settings import DEFAULT_FROM_EMAIL
from django.apps import apps

@shared_task
def add(x, y):
    return x + y

@shared_task
def send_mail(task_id, updated):
    # todo: determine if this version of task is the latest, if so send mail. maybe just delete previous task is exists in save()?
    Task = apps.get_model('tasks', 'Task')
    task = Task.objects.get(id=task_id)
    return updated, str(task.updated)
    # send_mail('halo', 'halo', DEFAULT_FROM_EMAIL, ['zagozdakonrad@gmail.com'], fail_silently=False)