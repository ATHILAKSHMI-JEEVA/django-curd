
from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_role"
    )
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name="users"
    )
    team = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name="role_permissions"
    )
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE,related_name="permission_roles"
    )

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="files/")
    owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="owned_files",
    null=True,
    blank=True
)
    team = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
