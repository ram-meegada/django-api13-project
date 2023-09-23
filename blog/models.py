from django.db import models 
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    age = models.IntegerField(default=None, null=True, blank=True)
    full_name = models.CharField(max_length=255,default=None, null=True, blank=True)

class Description(models.Model):
    written_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='des')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    def __str__(self):
        return self.description

class Course(models.Model):
    course_opters = models.ManyToManyField(User, related_name='crs')
    course = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.course

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'captain' )
    friend = models.ManyToManyField(User)        
    def __str__(self):
        return self.user.username
    
# class Verification(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='veriff')
#     is_verified = models.BooleanField(default=False)    