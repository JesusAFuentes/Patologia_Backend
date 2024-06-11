from rest_framework import routers
from apps.user import views


router = routers.SimpleRouter()
router.register('users', views.UserViewSet, 'users')
urlpatterns = [
] + router.urls
