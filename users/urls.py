from django.urls import path
from .views import user_get
from .views import user_post
from .views import user_delete
from .views import user_update

urlpatterns = [
    path("users/", user_get, name="user_get"),
    path("users/create/",user_post),
    path("users/delete/<int:id>/",user_delete),
    path("users/update/<int:id>/",user_update)
    
]