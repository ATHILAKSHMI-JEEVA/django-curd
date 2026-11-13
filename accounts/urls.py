from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_account/',views.account_create),
    path('account_get/',views.account_get),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('user/create/',views.user_create,name="user_create")
]