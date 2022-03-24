from rest_framework import routers

from api.views import TaskViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)