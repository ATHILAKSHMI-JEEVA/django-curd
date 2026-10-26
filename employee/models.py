from django.db import models


class  Employee(models.Model):
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    native=models.CharField(max_length=100)
    photo=models.TextField(null=True,blank=True)

    def __str__(self):
       return self.name