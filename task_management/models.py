from django.db import models
from django.contrib.auth.hashers import make_password,check_password

class CustomUser(models.Model):
    ROLE=[("admin","Admin"),("client","Client"),]
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=150)
    role=models.CharField(max_length=50,choices=ROLE)
    is_active=models.BooleanField(default=True)

    def set_password(self,raw_password):
        self.password=make_password(raw_password)

    def check_password(self,raw_password):
        return check_password(raw_password,self.password)

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS=[("pending","Pending"),
            ("in_progress","In Progress"),
            ("completed","Completed")
            ]
    title=models.CharField(max_length=200)
    discription=models.TextField()
    assigned_to=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assigned_task")
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="created_tasks")
    status=models.CharField(max_length=20,choices=STATUS,default="pending")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    completion_proof = models.FileField(
    upload_to="completion_proofs/",
    blank=True,
    null=True
    )

    def __str__(self):
        return self.title

class TaskHistory(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="history"
    )

    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    changed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    changed_at = models.DateTimeField(auto_now_add=True)