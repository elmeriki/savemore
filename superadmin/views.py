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
from superadmin.models import *
from stock.models import *
import string 
from random_id import random_id
from cashiers.models import *


@login_required(login_url='/')  
def approve_accountView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        new_account_list = User.objects.filter(is_activation=False,is_customer=False).exclude(is_superuser=True).exclude(is_ceo=True) | User.objects.filter(is_activation=True,is_customer=False).exclude(is_superuser=True).exclude(is_ceo=True)
        data = {
        'new_account_list':new_account_list
        }
        return render(request,'customer/approve_account.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def change_passwordView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/change_password.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def change_password_View(request):
    if request.user.is_authenticated and request.method=="POST" and request.user.is_ceo or request.user.is_admin:
        phone = request.POST['phone']
        password = request.POST['password']
        user_instance = User.objects.get(username=phone)
        user_instance.set_password(password)
        user_instance.save()
        messages.info(request,'Cashier Password has been updated successfully') 
        return redirect('/change_password')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def supervisorsView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        supervisor_list =User.objects.filter(is_supervisor=True).exclude(is_superuser=True).exclude(is_ceo=True).exclude(is_customer=True).exclude(is_admin=True).exclude(is_marketer=True).exclude(is_cashier=True).exclude(is_stock=True)
        data = {
        'supervisor_list':supervisor_list
        }
        return render(request,'customer/supervisor_list.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def cashier_orderView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        cashier_orders =CashierOrders.objects.filter(amount=0)[:30]
        data = {
        'cashier_orders':cashier_orders
        }
        return render(request,'customer/cashier_orders.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def delete_cashier_orderView(request,cashierorid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        delete_cashier_order=CashierOrders.objects.filter(cashierorid=cashierorid).delete()
        if delete_cashier_order:
            messages.info(request,'Cashier order has been deleted successfully') 
            return redirect('/cashier_order')
    else:
        return redirect('/cashier_order')


@login_required(login_url='/')  
def cashier_permisionView(request,userid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        user_permision_list = Cashierpermision.objects.filter(customer=userid)
        data = {
            'userid':userid,
            'user_permision_list':user_permision_list
        }
        return render(request,'customer/add_permision.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def supervisor_permisionView(request,userid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        supervisor_instance=User.objects.get(id=userid)
        supervisor_username=supervisor_instance.username
        supervisor_permision_list=User.objects.filter(is_cashier=True,supervisor=supervisor_username)
        list_of_cashiers=User.objects.filter(is_activation=True,is_cashier=True).filter(supervisor="None")
        data = {
            'userid':userid,
            'supervisor_permision_list':supervisor_permision_list,
            'list_of_cashiers':list_of_cashiers
        }
        return render(request,'customer/add_supervisor_permision.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional  
def delete_cashier_permissionView(request,userid,types):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        delete_cashiere_permision =Cashierpermision.objects.filter(customer=userid,types=types).delete()
        if delete_cashiere_permision:
            messages.info(request,'Permision has been deleted successfuly') 
            return redirect(f'/cashier_permision/{userid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional  
def delete_supervisor_permissionView(request,userid,supervisorid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        supervisor_instance=User.objects.get(username=supervisorid)
        delete_supervisor_permision=User.objects.get(id=userid)
        delete_supervisor_permision.supervisor="None"
        delete_supervisor_permision.save()
        messages.info(request,'Permision has been deleted successfuly') 
        return redirect(f'/supervisor_permision/{supervisor_instance.id}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional  
def save_cashier_permisionView(request,userid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        if request.method == "POST":
            types = request.POST['types']
            cashier_instance = User.objects.get(id=userid)
            if Cashierpermision.objects.filter(types=types,customer=cashier_instance).exists():
                messages.info(request,'Permision has been added already') 
                return redirect(f'/cashier_permision/{userid}')
            else:
                save_cashiere_permision = Cashierpermision(types=types,customer=cashier_instance)
                if save_cashiere_permision:
                    save_cashiere_permision.save()
                    messages.info(request,'Supervisor Permision added successfully.') 
                return redirect(f'/cashier_permision/{userid}')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional  
def save_supervisor_permisionView(request,userid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        if request.method == "POST":
            add_cashiers=request.POST['add_cashiers']
            supervisor_instance=User.objects.get(id=userid)
            cashier_instance=User.objects.get(username=add_cashiers)
            if User.objects.filter(username=cashier_instance.username,supervisor=supervisor_instance.username).exists():
                messages.info(request,'Permision has been added already') 
                return redirect(f'/supervisor_permision/{userid}')
            else:
                supervisor_instance=User.objects.get(id=userid)
                cashier_instance.supervisor=supervisor_instance.username
                cashier_instance.save()
                messages.info(request,'Supervisor Permision added successfully.') 
                return redirect(f'/supervisor_permision/{userid}')
    else:
        return redirect('/')

@login_required(login_url='/')  
def promotionView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin or request.user.is_customer:
        promo_messages = Promotion.objects.filter(status=0).order_by('-created_at')[:6]
        data = {
            'promo_messages':promo_messages
        }
        return render(request,'customer/promotion.html',context=data)

@login_required(login_url='/')  
def send_promoView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/send_promo.html')

@transaction.atomic
@login_required(login_url='/')  
def send_to_all_customer_promoView(request):
    if request.method =="POST" and request.POST['title'] and request.POST['message'] and request.POST['slogan'] and request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        title =request.POST['title']
        slogan =request.POST['slogan']
        message =request.POST['message']
        all_customers = User.objects.filter(is_activation=True).exclude(is_superuser=True) or User.objects.filter(is_activation=False).exclude(is_superuser=True)
        if all_customers:
            for each_customer in all_customers:
                customer_instance = User.objects.get(id=each_customer.id)
                send_single_promo_message = Promotion(customer=customer_instance,title=title,message=message,salestitle=slogan)
                send_single_promo_message.save()
               
        messages.info(request,'Promo message sent successfully')
        return redirect('/send_promo')
    else:
        messages.info(request,'Enter Value')
        return redirect('/send_promo')
    
@login_required(login_url='/')  
def approved_accountView(request,id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        activate_status = User.objects.filter(id=id).update(is_activation=True)
        if activate_status:
            return redirect('/approve_account')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def activate_supervisor_accountView(request,id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        activate_status = User.objects.filter(id=id).update(is_activation=True)
        if activate_status:
            return redirect('/supervisors')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def diactivate_accountView(request,id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        diactivate_status = User.objects.filter(id=id).update(is_activation=False)
        if diactivate_status:
            return redirect('/approve_account')
    else:
        return redirect('/')

@login_required(login_url='/')  
def diactivate_supervisor_accountView(request,id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        diactivate_status = User.objects.filter(id=id).update(is_activation=False)
        if diactivate_status:
            return redirect('/supervisors')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def expenses_displayView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        all_expenses = Expenses.objects.filter(status=0)
        if all_expenses:
            data = {
            'all_expenses':all_expenses 
            }
            return render(request,'customer/expenses_display.html',context=data)
        else:
            return redirect('/expenses_display')
    return redirect('/expenses_display')
    

@login_required(login_url='/')  
def dailysales_displayView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        all_sales=Sales.objects.filter(status=0)
        if all_sales:
            data = {
            'all_sales':all_sales 
            }
            return render(request,'customer/dailysales_display.html',context=data)
        else:
            return redirect('/dailysales_display')
    
@login_required(login_url='/')  
def expensesView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/expenses.html')
    
@login_required(login_url='/')  
def save_daily_SalesView(request):
    if request.user.is_authenticated and request.method =="POST" and request.POST['branch'] and request.POST['amount']  and request.POST['message'] and request.user.is_ceo or request.user.is_admin:
        branch = request.POST['branch']
        amount = float(request.POST['amount'])
        message = request.POST['message']
        save_daily_sales=Sales(customer=request.user,branch=branch,amount=amount,message=message)
        if save_daily_sales:
            save_daily_sales.save()
            messages.info(request,'Save Sales successfully')
            return render(request,'customer/daily_sales.html')
        else:
            messages.info(request,'Something went wrong')
            return render(request,'customer/daily_sales.html')
    else:
        return render(request,'customer/daily_sales.html')

    
@login_required(login_url='/')  
def save_daily_expensesView(request):
    if request.user.is_authenticated and request.method =="POST" and request.POST['branch'] and request.POST['title']  and request.POST['amount']  and request.POST['message'] and request.user.is_ceo or request.user.is_admin:
        branch=request.POST['branch']
        title=request.POST['title']
        amount=float(request.POST['amount'])
        message=request.POST['message']
        save_daily_expenses=Expenses(customer=request.user,branch=branch,amount=amount,title=title,message=message)
        if save_daily_expenses:
            save_daily_expenses.save()
            messages.info(request,'Save expenses successfully')
            return render(request,'customer/expenses.html')
        else:
            messages.info(request,'Something went wrong')
            return render(request,'customer/expenses.html')
    else:
        return render(request,'customer/expenses.html')

@login_required(login_url='/')  
def dailysalesView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/daily_sales.html')
    

@login_required(login_url='/')  
def search_productView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin or request.user.is_customer :
        search_text = request.POST.get('search_text')
        search_result = Stock.objects.filter(description__icontains=search_text)[:20] 
        if search_result:
            data = {
            'search_result':search_result
            }
        return render(request,'customer/search_result.html',context=data)
    else:
        return redirect('/invoice')
    
@login_required(login_url='/')  
def add_to_cartView(request,id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin or request.user.is_customer:
        customer_username = request.user.username
        customer_instance = User.objects.get(username=customer_username)
        if not Order.objects.filter(customer=customer_instance,status=0):
            orderid = random_id(length=7,character_set=string.digits)
            create_new_order = Order(customer=customer_instance,orderid=orderid)
            create_new_order.save()
        customer_order_id_instance = Order.objects.filter(status=0,customer=customer_instance)
        for orderid in customer_order_id_instance:
            for each_product in Stock.objects.filter(auto_increment_id=id):
                if Myorders.objects.filter(orderid=orderid.orderid,description=each_product.description).exists():
                    return HttpResponse("<button type='button' class='btn btn-success'>Added Already</button>")
                save_orders = Myorders(customer=customer_instance,orderid=orderid.orderid,description=each_product.description,stocktype=each_product.stockcode,excltotal=each_product.excl,excl=each_product.excl,incl=each_product.incl,incltotal=each_product.incl)
                if save_orders:
                    save_orders.save()
            return HttpResponse("<button type='button' class='btn btn-success'>Added successful</button>")
    else:
        return redirect('/invoice')
    
@login_required(login_url='/')  
def admin_order_listView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        order_list = Order.objects.all()
        if order_list:
            data = {
            'order_list':order_list 
            }
            return render(request,'customer/admin_order_list.html',context=data)
        else:
            return redirect('/')
    
    
@login_required(login_url='/')  
def admin_order_detailView(request,order_id):
    if request.user.is_authenticated and request.user.is_customer or request.user.is_admin:
        order_details = Myorders.objects.filter(orderid=order_id,status=0)
        incl = Myorders.objects.filter(orderid=order_id,status__gte=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(orderid=order_id,status__gte=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)
        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'fetch_order_id':order_id,
                'order_status':order_status
            }
            
        return render(request,'customer/admin_order_details.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def admin_edith_order_detailView(request,order_id):
    if request.user.is_authenticated and request.user.is_customer or request.user.is_admin:
        order_details = Myorders.objects.filter(orderid=order_id,status=0)
        incl = Myorders.objects.filter(orderid=order_id,status__gte=0).aggregate(Sum('incltotal'))['incltotal__sum']
        excl = Myorders.objects.filter(orderid=order_id,status__gte=0).aggregate(Sum('excltotal'))['excltotal__sum']
        order_status=Order.objects.values_list('status',flat=True).get(orderid=order_id)
        if order_details:
            data ={
                'order_details':order_details,
                'incl':incl,
                'excl':excl,
                'fetch_order_id':order_id,
                'order_status':order_status
            }
            
        return render(request,'customer/admin_edith_order.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def admin_update_order_detailView(request,id,qty,orderid):
    if request.user.is_authenticated and request.user.is_customer or request.user.is_admin and request.method =="POST" and request.POST['priceincl']:
        priceincl = int(request.POST['priceincl'])
        newpriceinc = priceincl * qty 
        update_inc_unit_price = Myorders.objects.filter(id=id,orderid=orderid).update(incl=priceincl)
        update_inc_new_total = Myorders.objects.filter(id=id,orderid=orderid).update(incltotal=newpriceinc)
        return redirect(f'/admin_edith_order_detail/{orderid}')
    else:
        return redirect('/')

@login_required(login_url='/')  
def process_orderView(request,order_id):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        data = {
        'order_id':Order.objects.values_list('orderid', flat=True).get(orderid=order_id)
        }
        return render(request,'customer/process_order.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def update_order_statusView(request):
    if request.user.is_authenticated and request.method == "POST" and request.user.is_ceo or request.user.is_admin:
        order_id = request.POST['order_id']
        status =request.POST['order_status_from_form']
        update_status = Order.objects.filter(orderid=order_id).update(adminstatus=status)
        if update_status:
                messages.info(request,'Successful')
                return redirect('/admin_order_list')
        else:
            return redirect('/')
        
@login_required(login_url='/')  
def chat_roomView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        customer_chat_message =Chatmessage.objects.filter(status=0).order_by('-created_at')
        if customer_chat_message:
            data = {
                'customer_chat_message':customer_chat_message
            }
        return render(request,'customer/chat_room.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def admin_chat_replyView(request,chatid):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        get_single_chat_message = Chatmessage.objects.filter(id=chatid,status=0)
        for get_single_chat_message  in get_single_chat_message:
            data= {
            'message':get_single_chat_message.message,
            'chatid':get_single_chat_message.id
            }
        return render(request,'customer/admin_message_reply.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def admin_response_messageView(request,chatid):
    if request.user.is_authenticated and request.method == "POST" and request.user.is_ceo or request.user.is_admin:
        message = request.POST['message']
        Chatmessage.objects.filter(id=chatid).update(response=message)
        update_status = Chatmessage.objects.filter(id=chatid).update(status=1)
        if update_status:
            return redirect('/chat_room')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def expenses_filterView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/expenses_filter.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def dialysales_filterView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        fetch_branches = Sales.objects.filter()
        data = {
        'fetch_branches':fetch_branches
        }
        return render(request,'customer/daily_sales_filter.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def fetch_daily_SalesView(request):
    if request.user.is_authenticated and request.method=="POST" and request.user.is_ceo or request.user.is_admin:
        branchname = request.POST['branch']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        fetch_sales = Sales.objects.filter(created_at__gte=startdate,created_at__lt=enddate).filter(branch=branchname)
        total_sales = Sales.objects.filter(created_at__gte=startdate,created_at__lt=enddate).filter(branch=branchname).aggregate(Sum('amount'))['amount__sum']
        all_Sales_from_branches =Sales.objects.filter(created_at__gte=startdate,created_at__lt=enddate)
        total_Sales_from_allbranches = Sales.objects.filter(created_at__gte=startdate,created_at__lt=enddate).aggregate(Sum('amount'))['amount__sum']

        if request.POST['branch'] == "allbranches":
            data={
            'fetch_sales':all_Sales_from_branches,
            'total_sales':total_Sales_from_allbranches
            }
            return render(request,'customer/daily_sales_filter.html',context=data)
        
        if not fetch_sales or all_Sales_from_branches:
            messages.info(request,'No Data Found')
            return redirect('/dialysales_filter')
        
        elif fetch_sales:
            data = {
            'fetch_sales':fetch_sales,
            'total_sales':total_sales
            }
            return render(request,'customer/daily_sales_filter.html',context=data)
    else:
        return redirect('/')
    
    

@login_required(login_url='/')  
def fetch_daily_expensesView(request):
    if request.user.is_authenticated and request.method=="POST" and request.user.is_ceo or request.user.is_admin:
        branchname = request.POST['branch']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        fetch_expenses = Expenses.objects.filter(created_at__gte=startdate,created_at__lt=enddate).filter(branch=branchname)
        total_expenses = Expenses.objects.filter(created_at__gte=startdate,created_at__lt=enddate).filter(branch=branchname).aggregate(Sum('amount'))['amount__sum']
        all_expenses_from_branches =Expenses.objects.filter(created_at__gte=startdate,created_at__lt=enddate)
        total_expenses_from_allbranches = Expenses.objects.filter(created_at__gte=startdate,created_at__lt=enddate).aggregate(Sum('amount'))['amount__sum']
        
        if request.POST['branch'] == "allbranches":
            data={
            'fetch_sales':all_expenses_from_branches,
            'total_sales':total_expenses_from_allbranches
            }
            return render(request,'customer/expenses_filter.html',context=data)
        
        if not fetch_expenses :
            messages.info(request,'No Data Found')
            return redirect('/expenses_filter')
        
        elif fetch_expenses:
            data = {
            'fetch_expenses':fetch_expenses,
            'total_expenses':total_expenses
            }
            return render(request,'customer/expenses_filter.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def search_customersView(request):
    if request.user.is_authenticated and request.user.is_ceo or request.user.is_admin:
        return render(request,'customer/search_customers.html')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def customer_searchView(request):
    if request.user.is_authenticated and request.method=="POST" and request.user.is_ceo or request.user.is_admin:
        city = request.POST['city']
        customer_list = User.objects.filter(is_customer=True,city=city)
        data = {
            'customer_list':customer_list
        }
        return render(request,'customer/search_customers.html',context=data)
    else:
        return redirect('/')