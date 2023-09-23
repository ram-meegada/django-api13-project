from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractUser):
    # age = models.PositiveIntegerField(_("age"))
    age = models.IntegerField(null=True, blank=True, verbose_name= "age of person")
    # location = models.CharField(max_length=255, null=True, blank=True)    