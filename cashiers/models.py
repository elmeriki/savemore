from django.db import models
from django.contrib.auth.models import AbstractUser
from savemauth.models import *

# Create your models here.
class Qadadic(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    bookno =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    description =  models.TextField(null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Qadadic"
        
    def __str__(self):
        return self.bookno
    
# Create your models here.
class Sts(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    recieptno =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "STS"
        
    def __str__(self):
        return self.recieptno
    
class Papers(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    pnumber =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    description =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "OTHER PAPERS"
        
    def __str__(self):
        return self.pnumber
    
class Notes(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    notenum =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    description =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "NOTES"
        
    def __str__(self):
        return self.notenum
    
    
class Swipes(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    swipsid =  models.TextField(null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    description =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "SWIPES"
        
    def __str__(self):
        return self.swipsid