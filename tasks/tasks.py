from celery import shared_task
from django.core.mail import send_mail

from company_tasks.settings import DEFAULT_FROM_EMAIL
from django.apps import apps


@shared_task
def schedule_mail(email, task_id, updated):
    Task = apps.get_model('tasks', 'Task')
    task = Task.objects.get(id=task_id)
    # second condition means if it's the latest version of email (it could be rescheduled then this task should be ignored)
    if task.state == task.TO_DO and updated == str(task.updated):
        send_mail('Minął czas wykonania zadania', f'{task}', DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    return updated, str(task.updated)
