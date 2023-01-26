from django.db import models
from django.contrib.auth.models import AbstractUser
from savemauth.models import *



class User(AbstractUser):
    is_ceo = models.BooleanField(default=False,blank=True,null=True)
    is_admin = models.BooleanField(default=False,blank=True,null=True)
    is_customer = models.BooleanField(default=False,blank=True,null=True)
    is_marketer = models.BooleanField(default=False,blank=True,null=True)
    is_activation = models.BooleanField(default=False,blank=True,null=True)
    is_stock = models.BooleanField(default=False,blank=True,null=True)
    is_cashier= models.BooleanField(default=False,blank=True,null=True)
    shopname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    city =  models.CharField(max_length=200,blank=True,null=True,default="None")
    shopaddress =  models.CharField(max_length=200,blank=True,null=True,default="None")
    branch =  models.CharField(max_length=200,blank=True,null=True,default="None")

    def __str__(self):
        return self.username
    
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'

