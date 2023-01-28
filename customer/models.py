from django.db import models
from django.contrib.auth.models import AbstractUser
from savemauth.models import *




    
# Create your models here.
class Promotion(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    title =  models.CharField(max_length=200,null=True,blank=True)
    message =  models.TextField(null=True,blank=True)
    salestitle =  models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Promotion Message"
        
    def __str__(self):
        return self.customer.first_name
    
# Create your models here.
class Chatmessage(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    message =  models.TextField(null=True,blank=True)
    response =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Chat Message"
        
    def __str__(self):
        return self.customer.first_name
    

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    orderid =  models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    adminstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Order IDs"
        
    def __str__(self):
        return self.customer.first_name
    
# Create your models here.
class Myorders(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    orderid =  models.CharField(max_length=200,null=True,blank=True)
    description =  models.CharField(max_length=200,null=True,default="None")
    stocktype =  models.CharField(max_length=200,null=True,default="None")
    excl = models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    excltotal = models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    quantity = models.IntegerField(null=True,blank=True,default=1)
    incl=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    incltotal=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Customer Orders"
        
    def __str__(self):
        return self.customer.first_name