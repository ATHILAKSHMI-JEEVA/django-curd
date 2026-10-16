from django.db import models


class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name