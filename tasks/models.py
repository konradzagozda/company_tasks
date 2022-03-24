from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT


class Task(models.Model):
    DONE = 'DONE'
    TO_DO = 'TO_DO'
    TASK_CHOICES = (
        (TO_DO, TO_DO),
        (DONE, DONE),
    )

    assigned_user = models.ForeignKey(User, on_delete=PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(choices=TASK_CHOICES, max_length=5, default=TO_DO)
    deadline = models.DateTimeField()
