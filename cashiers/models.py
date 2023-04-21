from django.db import models
from django.contrib.auth.models import AbstractUser
from savemauth.models import *

class Saleslog(models.Model):
    cashier = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    grandtotal=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    totalpertype=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    diff=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    comment = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "SALES LOG"
        
    def __str__(self):
        return self.cashier.first_name

# Create your models here.
class CashierOrders(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    types = models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    comment = models.TextField(null=True,blank=True,default="NA")
    adminstatus = models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    actualamount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
        
    def __str__(self):
        return self.types
        
    class Meta:
        verbose_name_plural = "CASHIER ORDERS"
    

# Create your models here.
class Qadadic(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid = models.CharField(max_length=200,default=0,null=True,blank=True)
    bookno =  models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=  models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "QADADIC"
        
    def __str__(self):
        return self.bookno

    
# Create your models here.
class Sts(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    bookno =  models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "STS"
        
    def __str__(self):
        return self.bookno
    
class Papers(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    bookno =  models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "OTHER PAPERS"
        
    def __str__(self):
        return self.bookno
    
class Notes(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "NOTES"
        
    def __str__(self):
        return self.cashierorid
    
    
class Swipes(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "SWIPES"
        
    def __str__(self):
        return self.cashierorid
    
class Kazang(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cashierorid =models.CharField(max_length=200,default=0,null=True,blank=True)
    amount=models.DecimalField(max_digits=11,decimal_places=0,default=0,blank=True,null=True)
    status = models.CharField(max_length=200,default=0,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        verbose_name_plural = "KAZANG"
        
    def __str__(self):
        return self.cashierorid
    
