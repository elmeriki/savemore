from django.db import models
from django.contrib.auth.models import AbstractUser
from savemauth.models import *


# Create your models here.
class Expenses(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    branch =  models.CharField(max_length=200,null=True,blank=True)
    title =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    message =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dail Expenses"
        
    def __str__(self):
        return self.customer.first_name
    
# Create your models here.
class Sales(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    branch =  models.CharField(max_length=200,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    message =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Daily Sales"
        
    def __str__(self):
        return self.customer.first_name