import random
from django.db import models
from django.contrib.auth.models import AbstractUser
# from account.models import CustomUser

# Create your models here.

class SubscriberType(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    TEACHER = "TEACHER", "Teacher"
    TEADER = "TEADER", "Trader"
    BANKER = "BANKER", "Banker"
    FARMER = "FARMER", "Farmer"
    BROKER = "BROKER", "Broker"
    OTHER = "OTHER", "Other"

class GenderType(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        UNSPECIFIED = "Unspecified", "Unspecified"
        OTHER = "OTHER", "OTHER"

class Company(models.Model):
     name = models.CharField(max_length=150,unique=False)
     coupon = models.CharField(max_length=15,unique=True)
     domain = models.CharField(max_length=200,blank=True,null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     def __str__(self):
          return self.name
     
class DefaultCompany(models.Model):
     name = models.CharField(max_length=150,unique=True)

class Subscriber(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField()
    ip = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone = models.CharField(max_length=50,null=True,blank=True)
    whatsapp = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    type =  models.CharField(
        max_length=20, choices=SubscriberType.choices, default=SubscriberType.OTHER
    )
    gender = models.CharField(max_length=20,choices=GenderType.choices,default=GenderType.UNSPECIFIED)
    age = models.CharField(max_length=4,null=True,blank=True)
    subscribed_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self) :
        return self.email

class CustomUser(AbstractUser):
    # Add your custom fields here
    company = models.ManyToManyField(Company)
    email_verified = models.BooleanField(default=False)
    
class Category(models.Model):
     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
     name = models.CharField(max_length=50)
     subscriber = models.ManyToManyField(Subscriber)

     def __str__(self):
          return self.name

class SMSCategory(models.Model):
     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
     name = models.CharField(max_length=50)
     subscriber = models.ManyToManyField(Subscriber)

     def __str__(self):
          return self.name

class EmailOTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"

    @classmethod
    def generate_otp(cls, user):
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        email_otp, _ = cls.objects.get_or_create(user=user)
        email_otp.otp = otp
        email_otp.save()
        return otp