from django.contrib.auth.models import User


def create_admin(username, email, password):
    try:
        u = User.objects.get(username=username)
        u.is_superuser = True
        u.save()
    except User.DoesNotExist:
        User.objects.create_superuser(username=username, email=email, password=password)
