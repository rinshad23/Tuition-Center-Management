from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    user_type=models.CharField(max_length=10,default=1,null=True)
    status=models.CharField(max_length=10,default=0,null=True)

    
class Course(models.Model):
    course_name=models.CharField(max_length=255,null=True)
    Fees=models.IntegerField(null=True)
    duration=models.CharField(max_length=255,null=True)
    syllabus=models.FileField(upload_to='files/',blank=True,null=True)

def valnum(value):
    phone_number=''
    if len(phone_number) != 10:
        raise ValidationError('Phone number must be 10 digits')

   
class Teacher(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    age=models.IntegerField(null=True)
    phone_number=PhoneNumberField(region='IN',blank=True,validators=[valnum])
    image=models.ImageField(upload_to='Timage',null=True,blank=True)
    
class Student(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='userasign')
    age=models.IntegerField(null=True)
    phone_number=PhoneNumberField(region='IN',blank=True)
    image=models.ImageField(upload_to='Simage',null=True,blank=True)
    teacher=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='teacherasign')

class Attendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    status = models.CharField(max_length=10,null=True)
    
class Stdattendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    status = models.CharField(max_length=10,null=True)

class Task(models.Model):
    taskname=models.CharField(max_length=255,null=True)
    startdate=models.DateField(null=True)
    enddate=models.DateField(null=True)
    teacher=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    
class Stask(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,null=True,related_name='submission')
    description=models.TextField(null=True)
    pdf=models.FileField(upload_to='files/',blank=True,null=True)
    

