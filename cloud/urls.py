from django.urls import path
from .views import create_cloud,get_cloud,get_obcloud,put_cloud,delete_cloud

urlpatterns=[
    path("cloud/",create_cloud,name="create_cloud"),
    path("cloud/get/",get_cloud,name="get_cloud"),
    path("cloud/<int:cloud_id>/get/",get_obcloud,name="get_obcloud"),
    path("cloud/<int:cloud_id>/update/", put_cloud, name="update_cloud"),
    path("cloud/<int:cloud_id>/delete/",delete_cloud,name="delete_cloud")
]