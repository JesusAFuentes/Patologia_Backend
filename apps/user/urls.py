from rest_framework import routers
from apps.user import views
from django.urls import path
from knox.views import LogoutView, LogoutAllView
from apps.user.views import LoginCustomView


router = routers.SimpleRouter()
router.register('users', views.UserViewSet, 'users')
urlpatterns = [
    path('auth/login/', LoginCustomView.as_view(), name='knox-custom-login'),
    path('auth/logout/', LogoutView.as_view(), name='knox-logout'),
    path('auth/logoutall/', LogoutAllView.as_view(), name='knox-logoutall'),
] + router.urls
