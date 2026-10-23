from django.db import models

class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    native=models.CharField(max_length=100)
    photo=models.BinaryField(null=True,blank=True)

def __str__(self):
    return self.name


#BinaryField is used to store binary data in the db.
#upload_to specifies the directory where the uploaded files will be stored.
#blank=True --photo optional
#null=true --photo can be null in the db