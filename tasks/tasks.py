from celery import shared_task
from celery.schedules import solar
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from company_tasks.celery import app
from company_tasks.settings import DEFAULT_FROM_EMAIL
from django.apps import apps


@shared_task
def schedule_mail(email, task_id, updated):
    Task = apps.get_model('tasks', 'Task')
    task = Task.objects.get(id=task_id)
    # second condition means if it's the latest version of email (it could be rescheduled then this task should be ignored)
    if task.state == task.TO_DO and updated == str(task.updated):
        send_mail('Minął czas wykonania zadania 😞', f'{task}', DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    return updated, str(task.updated)


@shared_task
def send_task_reminders():
    Task = apps.get_model('tasks', 'Task')
    User = get_user_model()
    users = User.objects.filter(is_superuser=False)
    for user in users:
        tasks = Task.objects.filter(assigned_user=user, state=Task.TO_DO)
        msg = 'Dzień dobry 🌞\n\nTwoja lista zadań do zrobienia:\n\n'
        for task in tasks:
            msg += f'\tTytuł: {task.title}\n'
            msg += f'\tOpis: {task.description}\n'
            msg += f'\tTermin wykonania: {task.deadline}\n\n'
        send_mail(
            'Lista zadań 📝',
            msg,
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )


app.conf.beat_schedule = {
    # Executes at sunset in Lublin
    'add-at-lublin-sunrise': {
        'task': 'tasks.tasks.send_task_reminders',
        'schedule': solar('sunrise', 51.246452, 22.568445),
    },
}