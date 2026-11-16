from django.urls import path
from .views import create_role, create_permision,assign_permision,get_role_permision,register_admin
from admin_client import views
urlpatterns = [
    path("create_role/", create_role, name="create_role"),
    path("create_permision/", create_permision, name="create_permision"),
    path("assign_permision/", assign_permision, name="assign_permision"),
    path("get_assign_permision/<int:role_id>/",get_role_permision,name="get_assign_permision"),
    path("register_admin/", register_admin, name="register_admin"),
    path("login/", views.login_user, name="login"),
    path("refresh_token/", views.refresh_access_token, name="refresh_token"),
    path("admin/client/create/", views.create_client, name="create_client"),
    path("admin/clients/", views.view_clients, name="view_clients"),
    path("admin/client/update/<int:user_id>/", views.update_client, name="update_client"),
    path("admin/client/delete/<int:user_id>/", views.delete_client),
    path("create_status/", views.create_status),
    path("admin/task/create/", views.create_task),
    path("admin/task/", views.view_tasks, name="view_tasks"),
    path("admin/task/update/<int:task_id>/", views.update_task),
    path("admin/task/delete/<int:task_id>/", views.delete_task),
    path("client/tasks/", views.client_view_tasks),
    path("client/task/update-status/<int:task_id>/", views.client_update_task_status),
    path("task/history/<int:task_id>/", views.view_task_history),
    path("client/dashboard/", views.client_dashboard),
    path(
    "client/task/upload-proof/<int:task_id>/",
    views.upload_task_proof
),
    path("client/tasks/search/", views.search_tasks, name="search_tasks"),
    path("admin/task/filter/", views.filter_tasks),
    path("admin/task/pagination/", views.pagination_tasks),
    path("admin/dashboard/", views.admin_dashboard),
    
]