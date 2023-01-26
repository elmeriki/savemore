from django.shortcuts import render
from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count,Sum
from django.db.models import Q
from django.urls import resolve
import datetime
from datetime import date
from django.core.mail import EmailMessage
import csv
from django.db.models import Q
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.views.generic import View
from savemauth.models import *
from stock.models import *
from stock.forms import *
from tablib import Dataset
from stock.resources import *
# Create your views here.



def stock_import_View(request):
    if request.method =="POST" and request.user.is_authenticated and request.user.is_ceo:
        if len(request.FILES) != 0:
            messages.info(request,'Select Product File')
            return redirect('/stock')
        
        newstocks = request.FILES['my_files']
        stockresources = StockResources()
        dataset = Dataset()
        importedata = dataset.load(newstocks.read(),format='xls')
        for data in importedata:
            value = Stock(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            data[9],
            data[10],
            data[11],
            data[12],
            data[13],
            data[14],
            )
            value.save()
            messages.info(request,'Loaded successfully')
            return redirect('/stock')
    else:
        return render(request,'customer/forms.html')