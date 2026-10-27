from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class File(models.Model):
    uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="uploaded_files")
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="files/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    manager = models.ForeignKey(User,on_delete=models.CASCADE,related_name="team_members")
    employee = models.OneToOneField(User,on_delete=models.CASCADE,related_name="team_manager")

    def __str__(self):
        return f"{self.employee.username} - {self.manager.username}"

