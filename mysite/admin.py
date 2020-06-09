from django.contrib import admin

# Register your models here.
from mysite.models import Student
from mysite.models import Attendance

admin.site.register(Student)
admin.site.register(Attendance)