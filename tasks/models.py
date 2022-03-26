from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT

from tasks.tasks import send_mail


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

    def __str__(self):
        return f'{self.title}\t{self.description[:30]}\t{self.deadline}\t{self.state}'

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        # todo: schedule sending mail
        send_mail.delay(self.id, self.updated)
