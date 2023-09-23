from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    user = models.ManyToManyField(User)
    course = models.CharField(max_length=255)
    def taken_by(self):
        people = []
        for i in self.user.all():
            people.append(str(i))
        return ','.join(people)