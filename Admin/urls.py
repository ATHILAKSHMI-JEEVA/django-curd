from .models import Admin
from .views import admin_get
from django.urls import path
from .views import admin_post
from .views import admin_delete
from .views import admin_update

urlpatterns = [
    path("admins/", admin_get, name="admin_get"),
    path("admins/create/", admin_post),
    path("admins/delete/<int:id>/", admin_delete),
    path("admins/update/<int:id>/", admin_update)

    
]