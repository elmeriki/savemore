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
from customer.models import *
from django.db.models import Sum

# Create your views here.


@login_required(login_url='/')  
def new_orderView(request):
    return render(request,'customer/new_order.html',{})



@login_required(login_url='/')  
def invoiceView(request):
    return render(request,'customer/invoices.html',{})



@login_required(login_url='/')  
def track_orderView(request):
    return render(request,'customer/track_order.html',{})


@login_required(login_url='/')  
def track_my_orderView(request):
    if request.user.is_authenticated  and request.user.is_customer or request.user.is_admin:
        if request.method=="POST":
            order_id = request.POST['orderid']
            username=request.user.username
            customer_instance =User.objects.get(username=username)
            order_status = Order.objects.filter(customer=customer_instance,orderid=order_id)
            if not order_status:
                messages.info(request,'Incorrect Order Number')
                return redirect('/track_order')
            else:
                
                data = {
                    'order_status':order_status
                }
                return render(request,'customer/track_order.html',context=data)
        else:
            return redirect('/track_order')


@login_required(login_url='/')  
def conversationView(request):
    if request.user.is_authenticated  and request.user.is_customer:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        chat_messages = Chatmessage.objects.filter(customer=customer_instance)
        data ={
            
            'chat_messages':chat_messages
        }
        return render(request,'customer/conversation.html',context=data)


@login_required(login_url='/')  
def list_customersView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        customer_list = User.objects.filter(is_customer=True)
        data = {
        'customer_list':customer_list
        }
        return render(request,'customer/customer_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def order_listView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin or request.user.is_customer:
        username =request.user.username 
        customer_instance = User.objects.get(username=username)
        order_list = Order.objects.filter(customer=customer_instance)
        data = {
        'order_list':order_list
        }
        return render(request,'customer/order_list.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def customer_promo_messageView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin or request.user.is_customer:
        username =request.user.username 
        customer_instance = User.objects.get(username=username)
        promo_messages = Promotion.objects.filter(customer=customer_instance,status=0)
        data ={
            'promo_messages':promo_messages
        }
        return render(request,'customer/customer_promo.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def order_detailView(request,order_id):
    if request.user.is_authenticated and request.user.is_customer or request.user.is_admin:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        order_details = Myorders.objects.filter(orderid=order_id,status=0)
        incl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)

        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'fetch_order_id':order_id,
                'order_status':order_status
            }
            
        return render(request,'customer/order_details.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def delete_single_orderView(request,order_id,id):
    if request.user.is_authenticated  and request.user.is_customer:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        Myorders.objects.filter(customer=customer_instance,id=id).delete()
        order_details = Myorders.objects.filter(orderid=order_id,status=0).filter(customer=customer_instance)
        incl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)

        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'order_status':order_status
            }
        return render(request,'customer/order_details.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def update_quantityView(request,order_id,id):
    if request.user.is_authenticated  and request.user.is_customer or request.user.is_admin:
        quantity = int(request.POST['quantity'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        Myorders.objects.filter(customer=customer_instance,id=id).update(quantity=quantity)
        incl_price =Myorders.objects.values_list('incl',flat=True).get(id=id)
        excl_price =Myorders.objects.values_list('excl',flat=True).get(id=id)
        new_excl_total = excl_price * quantity
        new_incl_total = incl_price * quantity
        Myorders.objects.filter(id=id).update(incltotal=new_incl_total)
        Myorders.objects.filter(id=id).update(excltotal=new_excl_total)
        order_details = Myorders.objects.filter(orderid=order_id,status=0).filter(customer=customer_instance)
        incl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)

        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'order_status':order_status
            }
        return render(request,'customer/order_details.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def update_order_statusView(request,order_id):
    if request.user.is_authenticated  and request.user.is_customer or request.user.is_admin:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        update_order_status = Order.objects.filter(customer=customer_instance,orderid=order_id).update(status=1)
        if update_order_status:
            return redirect('/order_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def chat_messageView(request):
    if request.user.is_authenticated  and request.user.is_customer:
        if request.method == "POST" and request.POST['message']:
            message = request.POST['message']
            username=request.user.username
            customer_instance =User.objects.get(username=username)
            save_chat_message =Chatmessage(customer=customer_instance,message=message,response="Process..")
            if save_chat_message:
                save_chat_message.save()
                return redirect('/conversation')
        else:
            return redirect('/conversation')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def delete_chat_messageView(request,id):
    if request.user.is_authenticated  and request.user.is_customer:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        delete_chat_message =Chatmessage.objects.filter(customer=customer_instance,id=id).delete()
        if delete_chat_message:
            return redirect('/conversation')
    else:
        return redirect('/conversation')

@login_required(login_url='/')  
def message_detailView(request,id):
    if request.user.is_authenticated  and request.user.is_customer:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        message_details = Promotion.objects.filter(customer=customer_instance,id=id)
        if message_details:
            data = {
                'message_details':message_details
            }
        return render(request,'customer/message_details.html',context=data)
    else:
        return render(request,'customer/message_details.html')
    
@login_required(login_url='/')  
def delete_promotional_messageView(request,id):
    if request.user.is_authenticated  and request.user.is_customer:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        delete_single_message = Promotion.objects.filter(customer=customer_instance,id=id).delete()
        if delete_single_message:
            return redirect('/customer_promo_message')
    else:
       return redirect('/customer_promo_message')
   
   
@login_required(login_url='/')  
def myinvoiceView(request):
    if request.user.is_authenticated  and request.user.is_customer or request.user.is_admin:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        promo_messages=Promotion.objects.filter(customer=customer_instance,status=0).order_by('-created_at')[:5]
        order_list = Order.objects.filter(customer=customer_instance,status=1)
        if order_list:
            data ={
             'order_list':order_list,
             'promo_messages':promo_messages
            }
            return render(request,'customer/myinvoice.html',context=data)
        else:
            return redirect('/customer_promo_message')
        
        

@login_required(login_url='/')  
def my_invoice_detailView(request,order_id):
    if request.user.is_authenticated and request.user.is_customer or request.user.is_admin:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        order_details = Myorders.objects.filter(orderid=order_id,status=0)
        incl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(customer=customer_instance,status=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)

        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'fetch_order_id':order_id,
                'order_status':order_status
            }
            
        return render(request,'customer/my_invoice_details.html',context=data)
    else:
        return redirect('/')