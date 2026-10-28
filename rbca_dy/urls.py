from django.urls import path
from . import views

urlpatterns = [
    path("users/create/", views.create_user, name="rbac_create_user"),
    path("roles/create/", views.create_role, name="create_role"),
    path("permissions/create/", views.create_permission, name="create_permission"),
    path("permissions/assign/", views.assign_permission, name="assign_permission"),
    path("users/assign-role/", views.assign_role, name="assign_role"),

    path("files/upload/", views.upload_file, name="upload_file"),
    path("files/view/", views.view_files, name="view_files"),
    path("files/<int:file_id>/update/", views.update_file, name="update_file"),
    path("files/<int:file_id>/delete/", views.delete_file, name="delete_file"),
    path("permissions/", views.get_permissions, name="get_permissions"),
]
