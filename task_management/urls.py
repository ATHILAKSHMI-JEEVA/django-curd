from django.urls import path
from .views import register_user,login_user,protected_api, update_task
from .views import create_admin,create_client,create_task,get_all_task,client_task_list,update_task_status,upload_completion_proof,client_dashboard
from .views import update_task,delete_task,update_client,delete_client,get_all_clients,single_client,admin_dashboard,client_task_history
urlpatterns=[
    path('register/',register_user,name="register_user"),
    path('login/',login_user,name="login_user"),
    path('protected/',protected_api,name="protected_api"),
    path('admin/',create_admin,name="create_admin"),
    path('admin/client/',create_client,name="create_client"),
    path('admin/task/create/',create_task,name="create_task"),
    path('admin/task/',get_all_task,name="get_all_task"),
    path('admin/task/<int:task_id>/update/',update_task,name="update_task"),
    path('admin/task/<int:task_id>/delete/',delete_task,name="delete_task"),
    path('admin/client/<int:client_id>/update/',update_client,name="update_client"),
    path('admin/client/<int:client_id>/delete/',delete_client,name="delete_client"),
    path('admin/client/get/',get_all_clients,name="get_all_clients"),
    path('admin/client/<int:client_id>/',single_client,name="single_client"),
    path('admin/dashboard/',admin_dashboard,name="admin_dashboard"),
    path('client/task/',client_task_list,name="client_task_list"),
    path('client/task/<int:task_id>/update/',update_task_status,name="update_task_status"),
    path('client/task/<int:task_id>/upload/',upload_completion_proof,name="upload_completion_proof"),
    path('client/task/<int:task_id>/history/',client_task_history,name="client_task_history"),
    path('client/dashboard/',client_dashboard,name="client_dashboard"),
]
