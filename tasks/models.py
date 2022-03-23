from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT


class Task(models.Model):
    TASK_CHOICES = (
        ('DONE', 'DONE'),
        ('TD_DO', 'TO_DO')
    )

    user = models.ForeignKey(User, on_delete=PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(choices=TASK_CHOICES, max_length=5)
    deadline = models.DateTimeField()
