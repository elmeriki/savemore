from django.db import models
from savemauth.models import *
# Create your models here.


class Stock(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    stockcode =  models.CharField(max_length=200,null=True,blank=True,default="None")
    linkcode =  models.CharField(max_length=200,null=True,blank=True,default="None")
    stocktype =  models.CharField(max_length=200,null=True,default="None")
    unit =  models.CharField(max_length=200,null=True,default="None")
    description =  models.CharField(max_length=200,null=True,default="None")
    barcode =  models.CharField(max_length=200,null=True,default="None")
    packsize = models.CharField(max_length=200,null=True,default="None")
    onhand = models.CharField(max_length=200,null=True,blank=True,default="None")
    avgcostexcl =models.CharField(max_length=200,null=True,blank=True,default="None")
    lastcostexcl = models.CharField(max_length=200,null=True,blank=True,default="None")
    excl = models.CharField(max_length=200,null=True,blank=True,default="None")
    incl = models.CharField(max_length=200,null=True,blank=True,default="None")
    defaultgp = models.CharField(max_length=200,null=True,blank=True,default="None")
    gp = models.CharField(max_length=200,null=True,blank=True,default="None")
    vat = models.CharField(max_length=200,null=True,blank=True,default="None")
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    class Meta:
        verbose_name_plural = "SaveMore Stock"
        
    def __str__(self):
        return self.description

