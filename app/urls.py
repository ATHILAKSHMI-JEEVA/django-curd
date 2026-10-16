
from django.urls import path
from .views import app_login
from .views import app_logout


urlpatterns = [
    path("app/", app_login),
    path("app/", app_logout)
]