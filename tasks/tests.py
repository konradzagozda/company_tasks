from django.core.mail import send_mail
from django.test import TestCase

from company_tasks.settings import DEFAULT_FROM_EMAIL


class MailTest(TestCase):
    def test_mail(self):
        send_mail('halo', 'halo', DEFAULT_FROM_EMAIL, ['zagozdakonrad@gmail.com'], fail_silently=False)