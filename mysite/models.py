from django.db import models
from django.utils.timezone import now

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    usn = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=30)
    mac = models.CharField(max_length=20)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.usn


class Attendance(models.Model):
    sno = models.AutoField(primary_key=True)
    mac = models.CharField(max_length=20)
    usn = models.CharField(max_length=20)
    # usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    date= models.DateField(default=now)
    time = models.TimeField(default=now)

