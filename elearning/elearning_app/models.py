from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    type = models.CharField(null=False, blank=False, max_length=256, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    first_name = models.CharField(null=False, blank=False, max_length=256)
    last_name = models.CharField(null=False, blank=False, max_length=256)
    email = models.EmailField(null=False, blank=False, max_length=256)
    photo = models.FileField(null=False, blank=False, upload_to='user_photos/')

class Course(models.Model):
    code = models.CharField(null=False, blank=False, max_length=256)
    name = models.CharField(null=False, blank=False, max_length=256)
    description = models.TextField(null=False, blank=False)
    teacher = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    students = models.ManyToManyField(AppUser, blank=True, related_name='students')

class Material(models.Model):
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE)
    file = models.FileField(null=False, blank=False, upload_to='course_materials/')

class Feedback(models.Model):
    student = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField(null=False, blank=False)

class Status(models.Model):
    student = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)

class Chat(models.Model):
    room_name = models.CharField(null=False, blank=False, max_length=256, unique=True)
    admin = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    members = models.ManyToManyField(AppUser, blank=False, related_name='members')
    chat_log = models.TextField(null=True, blank=True)

class EnrolNotification(models.Model):
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE)
    student = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    teacher = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE, related_name='teacher')
    read = models.BooleanField(null=False, blank=False)

class MaterialNotification(models.Model):
    material = models.ForeignKey(Material, null=False, blank=False, on_delete=models.CASCADE)
    student = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    read = models.BooleanField(null=False, blank=False)