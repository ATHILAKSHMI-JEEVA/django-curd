from django.urls import path
from .views import test_permission,manager_test,employee_test
from .views import upload_file,get_my_files,get_all_files,manager_files,delete_my_file
from .views import admin_delete_file,manager_delete_file
from .views import admin_download_file

urlpatterns=[
    path("test-permission/",test_permission,name="test_permission"),
    path("manager-test/", manager_test, name="manager_test"),
    path("employee-test/",employee_test,name="employee_test"),
    path("upload-file/", upload_file, name="upload_file"),
    path("my-files/", get_my_files, name="get_my_files"),
    path("all-files/", get_all_files, name="get_all_files"),
    path("manager-files/", manager_files, name="manager_files"),
    path("my-files/<int:file_id>/delete/", delete_my_file, name="delete_my_file"),
    path("admin-files/<int:file_id>/delete/", admin_delete_file, name="admin_delete_file"),
    path("manager-files/<int:file_id>/delete/",manager_delete_file,name="manager_delete_file"),
    path("admin_files/<int:file_id>/download/",admin_download_file,name="admin_download_file"),
]