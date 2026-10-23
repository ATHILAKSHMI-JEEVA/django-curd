

from django.urls import path
from .views import create_student
from .views import get_student
from .views import get_student_photo
from .views import update_student
from .views import delete_student

urlpatterns = [
    path("students/create/",create_student,name="create_student"),
    path("students/",get_student, name="get_students"),
     path(
        "students/<int:student_id>/photo/",
        get_student_photo,
        name="get_student_photo"
    ),
    path("students/<int:student_id>/",update_student, name="update_student"),
    path("students/<int:student_id>/delete/",delete_student, name="delete_student")
]