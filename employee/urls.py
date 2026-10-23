
from django.urls import path
from .views import employee_create,employee_get,employee_photo,employee_update,employee_delete

urlpatterns =[
    path('employee/',employee_create,name="employee_create"),
    path('employee/get/',employee_get,name="employee_get"),
    path("employee/<int:employee_id>/photo/",employee_photo,name="employee_photo"),
    path("employee/<int:employee_id>/update/",employee_update,name="employee_update"),
    path("employee/<int:employee_id>/delete/",employee_delete,name="employee_delete"),
]