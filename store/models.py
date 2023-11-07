#models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    medical_certificate = models.CharField(max_length=20)
    guardian_type = models.CharField(max_length=20)# Add any additional fields you need
    def __str__(self):
        return self.username

class Doctor(models.Model):  
     name = models.CharField(max_length=20) 
     username = models.CharField(max_length=30)
     email = models.CharField(max_length=20)   
     phone = models.CharField(max_length=20) 
     password = models.CharField(max_length=20) 
     qualification = models.CharField(max_length=20)
     specialization = models.CharField(max_length=20)   
def __str__(self):
        return self.username



