from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    # profile_pic = models.ImageField(upload_to="media/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    Address_line1 = models.CharField(max_length=255, null=True, blank=True, default=None)
    Address_line2 = models.CharField(max_length=255, null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userpayment')
    card_number = models.IntegerField(null=False, blank=False)
    card_holdername = models.CharField(max_length=255, null=True, blank=True)
    expiry_date = models.DateField(null=False, blank=False)    

CATEGORY_CHOICES=(("1","Contracts"),("2","Trust"),("3","Deeds"),("4","Common loan Documents"),("5","Affidavits"),
                  ("6","Vehicle certificate of ownership"), ("7","Acknowledgement"), ("8","Identity verifications")) 
NOTARYMETHOD_CHOICES = (("1", "online"),("2", "offline"))   
DOCUMENTUPLOAD_CHOICES = (("1", "Pickup"),("2","Download from app"))
SESSION_STATUS_CHOICES = (("1","Completed"),("2","In Progress"),("3","Cancelled"),("4","Not started"))

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="1")
    full_name = models.CharField(max_length=255, null=True, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    Address_line1 = models.CharField(max_length=255, null=False, blank=False)
    Address_line2 = models.CharField(max_length=255)
    notary_method = models.CharField(max_length=255, choices=NOTARYMETHOD_CHOICES, default=None, null=False, blank=False)
    documentupload_method = models.CharField(max_length=255, choices=DOCUMENTUPLOAD_CHOICES, default="2", null=False, blank=False)
    # live_session_status = models.CharField(max_length=255, choices=SESSION_STATUS_CHOICES, default="4")

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    Notary_agent_name = models.CharField(max_length=255, default=None)
    service_name = models.CharField(max_length=255, default=None)
    Notary_agent_charges = models.IntegerField(default=None)
    Customer_name = models.CharField(max_length=255, default=None)
    Commission_Number = models.CharField(max_length=15, default=None)
    Delivery_charges = models.IntegerField(default=10)
    Service_charges = models.IntegerField(default=20)
    Total = models.IntegerField(default=None)
    status = models.CharField(max_length=255, choices=SESSION_STATUS_CHOICES, default="4")    

class order(models.Model):
    pass    