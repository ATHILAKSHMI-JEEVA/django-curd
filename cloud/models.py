from django.db import models

class Cloudstorage(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    native=models.CharField(max_length=100)
    photo=models.ImageField(upload_to="clouds/",null=True,blank=True)

    def __str__(self):
        return self.name
 

