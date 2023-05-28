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
from cashiers.models import *

@login_required(login_url='/')  
def supervisor_dashboardView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        cashier_list =User.objects.filter(is_cashier=True)
        data  = {
        'cashier_list':cashier_list
        }
        return render(request,'supervisor/supervisor_dashboard.html',context=data)
    
@login_required(login_url='/')  
def supervisor_profileView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        return render(request,'supervisor/supervisor_profile.html',{})
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def single_cashierView(request,userid):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_ceo :
        fetch_cashier_instance=User.objects.get(id=userid)
        fetch_data_single_cashier = CashierOrders.objects.filter(customer=fetch_cashier_instance,adminstatus=0)
        fetch_cashier_names =(User.objects.values_list('first_name', flat=True).get(id=userid))

        data = {
        'fetch_data_single_cashier':fetch_data_single_cashier,
        'fetch_cashier_names':fetch_cashier_names,
        'fetch_cashier_instance':fetch_cashier_instance
        }
        return render(request,'supervisor/single_cashier.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def single_cashier_ceoView(request,userid):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_ceo :
        fetch_cashier_instance=User.objects.get(id=userid)
        fetch_data_single_cashier_ceo = CashierOrders.objects.filter(customer=fetch_cashier_instance,adminstatus=2)
        data = {
        'fetch_data_single_cashier_ceo':fetch_data_single_cashier_ceo  
        }
        return render(request,'supervisor/single_cashier.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def process_actualView(request,orderid,type,customerid):
    if request.user.is_authenticated and request.user.is_supervisor:
        data = {
            'orderid':orderid,
            'type':type,
            'customerid':customerid
        }
        return render(request,'supervisor/process_actual.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def process_actual_saveView(request,orderid,type,customerid):
    if request.user.is_authenticated and request.user.is_supervisor and request.method=="POST":
        amount=float(request.POST['amount'])
        curent_Amount = float(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=orderid))
        if amount < curent_Amount or amount > curent_Amount:
            messages.info(request,'TOTAL AMOUNT AND ACTUAL AMOUNT ARE NOT MATCHING')
            return redirect(f'/process_actual/{orderid}/{type}/{customerid}')
        if amount == curent_Amount:
            CashierOrders.objects.filter(cashierorid=orderid).update(actualamount=amount)
            CashierOrders.objects.filter(cashierorid=orderid).update(adminstatus=1)
            CashierOrders.objects.filter(cashierorid=orderid).update(status=1)
            if type == "Qadadic":
                Qadadic.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Sts":
                Sts.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Papers":
                Papers.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Note":
                Notes.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Kazang":
                Kazang.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Swipes":
                Swipes.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Acc":
                Acc.objects.filter(cashierorid=orderid).update(status=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def processed_logView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        return render(request,'supervisor/processed_log.html')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def processed_salesView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        date_from = datetime.datetime.now() - datetime.timedelta(days=2)
        supervisor_response_check=CashierOrders.objects.filter(adminstatus=0,created_at__gt=date_from).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(adminstatus=1,created_at__gt=date_from).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2,created_at__gt=date_from).count()
        qadadic_total_sum = Qadadic.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum=0
        else:
            pass
        
        sts_total_sum =Sts.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum = 0
        else:
            pass
        
        note_total_sum = Notes.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum =0
        else:
            pass
        
        papers_total_sum = Papers.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum=0
        else:
            pass
        swipes_total_sum = Swipes.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        acc_total_sum = Acc.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if acc_total_sum is None:
            acc_total_sum=0
        else:
            pass
        kazang_total_sum =Kazang.objects.filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if kazang_total_sum is None:
            kazang_total_sum=0
        else:
            pass
        cashier_list =User.objects.filter(is_cashier=True)
        if qadadic_total_sum is None:
            data = {
            'supervisor_response_check':supervisor_response_check,
            'supervisor_salesrecod_check':supervisor_salesrecod_check,
            'supervisor_salesrecod_check_':supervisor_salesrecod_check_,
            'qadadic_total_sum':qadadic_total_sum,
            'sts_total_sum':sts_total_sum ,
            'note_total_sum':note_total_sum,
            'papers_total_sum':papers_total_sum,
            'kazang_total_sum':kazang_total_sum,
            'swipes_total_sum':swipes_total_sum,
            'acc_total_sum':acc_total_sum,
            'cashier_list':cashier_list
            }
            return render(request,'supervisor/processed_sales.html',context=data)
        else:
            grand_total = acc_total_sum + qadadic_total_sum + sts_total_sum + note_total_sum + papers_total_sum + swipes_total_sum + kazang_total_sum
            data = {
            'supervisor_response_check':supervisor_response_check,
            'supervisor_salesrecod_check':supervisor_salesrecod_check,
            'supervisor_salesrecod_check_':supervisor_salesrecod_check_,
            'qadadic_total_sum':qadadic_total_sum,
            'sts_total_sum':sts_total_sum ,
            'note_total_sum':note_total_sum,
            'papers_total_sum':papers_total_sum,
            'kazang_total_sum':kazang_total_sum,
            'swipes_total_sum':swipes_total_sum,
            'acc_total_sum':acc_total_sum,
            'grand_total':grand_total,
            'cashier_list':cashier_list
            }
            return render(request,'supervisor/processed_sales.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def single_processed_salesView(request,userid):
    if request.user.is_authenticated and request.user.is_supervisor:
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        fetch_cashier_instance=User.objects.get(id=userid)
        supervisor_response_check=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(adminstatus=0,created_at__gt=date_from).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(adminstatus=1,created_at__gt=date_from).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2,created_at__gt=date_from).count()
        supervisor_salesrecod_check_count=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(~Q(adminstatus=0),created_at__gt=date_from).count()
        cashier_permissioncount = Cashierpermision.objects.filter(customer=fetch_cashier_instance).count()
        qadadic_total_sum=Qadadic.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum=0
        else:
            pass
        sts_total_sum =Sts.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum=0
        else:
            pass
        note_total_sum = Notes.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum=0
        else:
            pass
        papers_total_sum = Papers.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum=0
        else:
            pass
        swipes_total_sum = Swipes.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        acc_total_sum = Acc.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if acc_total_sum is None:
            acc_total_sum=0
        else:
            pass
        kazang_total_sum = Kazang.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if kazang_total_sum is None:
            kazang_total_sum=0
    
        grand_total = qadadic_total_sum + acc_total_sum + sts_total_sum + note_total_sum + papers_total_sum + swipes_total_sum + kazang_total_sum
        data = {
            'supervisor_response_check':supervisor_response_check,
            'supervisor_salesrecod_check':supervisor_salesrecod_check,
            'supervisor_salesrecod_check_':supervisor_salesrecod_check_,
            'qadadic_total_sum':qadadic_total_sum,
            'sts_total_sum':sts_total_sum ,
            'note_total_sum':note_total_sum,
            'papers_total_sum':papers_total_sum,
            'kazang_total_sum':kazang_total_sum,
            'swipes_total_sum':swipes_total_sum,
            'acc_total_sum':acc_total_sum,
            'grand_total':grand_total,
            'userid':userid,
            'cashier_permissioncount':cashier_permissioncount,
            'supervisor_salesrecod_check_count':supervisor_salesrecod_check_count,
            'fetch_cashier_instance':fetch_cashier_instance
            }
        return render(request,'supervisor/single_sales_log.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def search_processed_logView(request):
    if request.user.is_authenticated and request.user.is_supervisor and request.method=="POST":
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        processed_orders=CashierOrders.objects.filter(created_at__range=(startdate,enddate),adminstatus=2)
        data = {
        'processed_orders':processed_orders,
        }
        return render(request,'supervisor/processed_log.html',context=data)
    else:
        return redirect('/')

    
@login_required(login_url='/')  
def view_single_processed_orderView(request,userid):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_ceo:
        fetch_cashier_instance=User.objects.get(id=userid)
        fetch_data_single_cashier = CashierOrders.objects.filter(customer=fetch_cashier_instance,adminstatus=1)
        data = {
        'fetch_data_single_cashier':fetch_data_single_cashier  
        }
        return render(request,'supervisor/single_cashier.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def processed_single_orderView(request,cashierorid,types):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_ceo:
        fetch_data_single_cashier = CashierOrders.objects.filter(cashierorid=cashierorid,adminstatus=2)
        data = {
        'types':types,
        'fetch_data_single_cashier':fetch_data_single_cashier
        }
        return render(request,'supervisor/single_process_orders.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def processed_qadadicView(request,cashierorid,type):
    if request.user.is_authenticated and request.user.is_supervisor:
        processed_data_single = CashierOrders.objects.filter(cashierorid=cashierorid,adminstatus=1)
        data = {
        'type':type,
        'processed_data_single':processed_data_single
        }
        return render(request,'supervisor/single_process_orders.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def record_salesView(request,userid,grand_total):
    if request.user.is_authenticated and request.user.is_supervisor:
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        supervisor_response_check=CashierOrders.objects.filter(adminstatus=0,created_at__gt=date_from).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(adminstatus=1,created_at__gt=date_from).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2,created_at__gt=date_from).count()
        
        qadadic_total_sum = Qadadic.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum =0
        else:
            pass 
        sts_total_sum =Sts.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum=0
        else:
            pass
        note_total_sum = Notes.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum=0
        else:
            pass
        papers_total_sum = Papers.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum =0
        else:
            pass
        swipes_total_sum = Swipes.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        
        kazang_total_sum = Kazang.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if kazang_total_sum is None:
            kazang_total_sum=0
        else:
            pass
        acc_total_sum = Acc.objects.filter(customer=userid).filter(status=1,created_at__gt=date_from).aggregate(Sum('amount'))['amount__sum']
        if acc_total_sum is None:
            acc_total_sum=0
        else:
            pass
        grand_total = qadadic_total_sum + acc_total_sum + sts_total_sum + note_total_sum + papers_total_sum + swipes_total_sum + kazang_total_sum
        data = {
        'supervisor_response_check':supervisor_response_check,
        'supervisor_salesrecod_check':supervisor_salesrecod_check,
        'supervisor_salesrecod_check_':supervisor_salesrecod_check_,
        'grand_total':grand_total,
        'userid':userid
        }
        return render(request,'supervisor/record_sales.html',context=data)
    else:
        return redirect('/')
    
@transaction.atomic
@login_required(login_url='/')  
def record_salessaveView(request,userid,gt):
    if request.user.is_authenticated and request.user.is_supervisor and request.method=="POST":
        sales_total = int(request.POST['amount']) + int((request.POST['diamount']))
        diamount = int((request.POST['diamount']))
        comment = request.POST['comment']
        customer_instance =User.objects.get(id=userid)
        diff_amount = sales_total - gt 
        if sales_total > gt:
            record_Sales=Saleslog(cashier=customer_instance,grandtotal=sales_total,diff=diff_amount,status="Short",totalpertype=gt,di=diamount,comment=comment)
            if record_Sales:
                record_Sales.save()
                CashierOrders.objects.filter(~Q(adminstatus=2),customer=customer_instance).update(adminstatus=2)
                messages.info(request,f'Sale has been recorded successfully. Please hold for a few minutes while the process is completed in the background')
                return redirect('/sales_log')
        if sales_total < gt:
            record_Sales=Saleslog(cashier=customer_instance,grandtotal=sales_total,diff=diff_amount,status="Over",totalpertype=gt,di=diamount,comment=comment)
            if record_Sales:
                record_Sales.save()
                CashierOrders.objects.filter(~Q(adminstatus=2),customer=customer_instance).update(adminstatus=2)
                messages.info(request,f'Sale has been recorded successfully. Please hold for a few minutes while the process is completed in the background')
                return redirect('/sales_log')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def sales_logView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        sales_log = Saleslog.objects.all()
        data = {
            'sales_log':sales_log
        }
        return render(request,'supervisor/sales_log.html',context=data)
    else:
        return redirect('/')