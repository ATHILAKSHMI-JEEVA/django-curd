# from django.urls import path
# from .views import user_list
# from .views import user_detail

# urlpatterns = [
#     path("users/", user_list),
#     path("users/<int:id>/", user_detail),
# ]
from django.urls import path
from .views import admin_list
from .views import admin_detail

urlpatterns = [
    path("myadmin/", admin_list),
    path("myadmin/<int:id>/", admin_detail),
]