from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Role(models.Model):
    role_name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.role_name

class Permision(models.Model):
    permision_name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.permision_name

class RolePermision(models.Model):
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    permision=models.ForeignKey(Permision,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.role_name} - {self.permision.permision_name}"

class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")

    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class TaskStatus(models.Model):
    status_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.status_name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    assigned_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assigned_tasks")

    status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,)

    completion_proof = models.FileField(upload_to="task_proofs/",blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    old_status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,related_name="old_task_history")

    new_status = models.ForeignKey(TaskStatus,on_delete=models.CASCADE,related_name="new_task_history")

    changed_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="status_changed_by")

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.new_status.status_name}"


