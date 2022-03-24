from django.test import TestCase

from tasks.utils import send_mail


class MailTest(TestCase):
    def test_mail(self):
        send_mail('halo', 'halo', to_emails=['zagozdakonrad@gmail.com'])