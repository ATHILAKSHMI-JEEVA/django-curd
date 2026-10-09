from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    age = models.IntegerField()
   

    def __str__(self):
        return self.username