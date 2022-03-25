from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimestampedModel):
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

    class Meta:
        ordering = ('-state', 'deadline')
