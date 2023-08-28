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
        supervisor_instance = request.user
        supervisor_username=supervisor_instance.username
        cashier_list =User.objects.filter(is_cashier=True,supervisor=supervisor_username)
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
                Qadadic.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Sts":
                Sts.objects.filter(cashierorid=orderid).update(status=1)
                Sts.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Papers":
                Papers.objects.filter(cashierorid=orderid).update(status=1)
                Papers.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Note":
                Notes.objects.filter(cashierorid=orderid).update(status=1)
                Notes.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Kazang":
                Kazang.objects.filter(cashierorid=orderid).update(status=1)
                Kazang.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Swipes":
                Swipes.objects.filter(cashierorid=orderid).update(status=1)
                Swipes.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
            if type == "Acc":
                Acc.objects.filter(cashierorid=orderid).update(status=1)
                Acc.objects.filter(cashierorid=orderid).update(done=1)
                messages.info(request,f'{type} HAS BEEN SUPERVISE SUCCESSFULLY')
                return redirect(f'/single_cashier/{customerid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def processed_logView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        data={
        'cashier_list':User.objects.filter(is_cashier=True)
        }
        return render(request,'supervisor/processed_log.html',context=data)
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def processed_salesView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        date_from = datetime.datetime.now() - datetime.timedelta(days=2)
        supervisor_response_check=CashierOrders.objects.filter(adminstatus=0).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(adminstatus=1).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2).count()
        qadadic_total_sum = Qadadic.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum=0
        else:
            pass
        
        sts_total_sum =Sts.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum = 0
        else:
            pass
        
        note_total_sum = Notes.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum =0
        else:
            pass
        
        papers_total_sum = Papers.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum=0
        else:
            pass
        swipes_total_sum = Swipes.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        acc_total_sum = Acc.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if acc_total_sum is None:
            acc_total_sum=0
        else:
            pass
        kazang_total_sum =Kazang.objects.filter(status=1,done=1).aggregate(Sum('amount'))['amount__sum']
        if kazang_total_sum is None:
            kazang_total_sum=0
        else:
            pass
        supervisor_instance=request.user
        supervisor_username=supervisor_instance.username
        cashier_list=User.objects.filter(is_cashier=True,supervisor=supervisor_username)
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
        # date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        fetch_cashier_instance=User.objects.get(id=userid)
        supervisor_response_check=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(adminstatus=0).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(adminstatus=1).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2).count()
        supervisor_salesrecod_check_count=CashierOrders.objects.filter(customer=fetch_cashier_instance).filter(adminstatus=1).count()
        cashier_permissioncount = Cashierpermision.objects.filter(customer=fetch_cashier_instance).count()
        
        Qadadic.objects.filter(done=1).update(done=2)
        qadadic_total_sum=Qadadic.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum=0
        else:
            pass
        Sts.objects.filter(done=1).update(done=2)
        sts_total_sum =Sts.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum=0
        else:
            pass
        
        Notes.objects.filter(done=1).update(done=2)
        note_total_sum = Notes.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum=0
        else:
            pass
        
        Papers.objects.filter(done=1).update(done=2)
        papers_total_sum = Papers.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum=0
        else:
            pass
        
        Swipes.objects.filter(done=1).update(done=2)
        swipes_total_sum = Swipes.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        Acc.objects.filter(done=1).update(done=2)
        acc_total_sum = Acc.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if acc_total_sum is None:
            acc_total_sum=0
        else:
            pass
        
        Kazang.objects.filter(done=1).update(done=2)
        kazang_total_sum = Kazang.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
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
        cashier_id=int(request.POST['cashier_name'])
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        cashier_instance = User.objects.get(id=cashier_id)
        if not CashierOrders.objects.filter(created_at__range=(startdate,enddate),adminstatus=2).filter(customer=cashier_instance):
            messages.info(request,f'NO DATA WAS FOUND')
            return redirect('/processed_log')
        else:
            processed_orders=CashierOrders.objects.filter(created_at__range=(startdate,enddate),adminstatus=2).filter(customer=cashier_instance)
            data = {
            'startdate':startdate,
            'enddate':enddate,
            'cashier_id':cashier_id,
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
        # date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        supervisor_response_check=CashierOrders.objects.filter(adminstatus=0).count()
        supervisor_salesrecod_check=CashierOrders.objects.filter(adminstatus=1).count()
        supervisor_salesrecod_check_=CashierOrders.objects.filter(adminstatus=2).count()
        
        qadadic_total_sum=Qadadic.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if qadadic_total_sum is None:
            qadadic_total_sum=0
        else:
            pass 
        sts_total_sum =Sts.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if sts_total_sum is None:
            sts_total_sum=0
        else:
            pass
        note_total_sum = Notes.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if note_total_sum is None:
            note_total_sum=0
        else:
            pass
        papers_total_sum = Papers.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if papers_total_sum is None:
            papers_total_sum =0
        else:
            pass
        swipes_total_sum = Swipes.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if swipes_total_sum is None:
            swipes_total_sum=0
        else:
            pass
        
        kazang_total_sum = Kazang.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
        if kazang_total_sum is None:
            kazang_total_sum=0
        else:
            pass
        acc_total_sum = Acc.objects.filter(customer=userid).filter(status=1,done=2).aggregate(Sum('amount'))['amount__sum']
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
        precoin = int((request.POST['precoin']))
        comment = request.POST['comment']
        customer_instance =User.objects.get(id=userid)
        diff_amount =  sales_total - int(gt) - int(precoin)
        if sales_total > int(gt):
            record_Sales=Saleslog(cashier=customer_instance,grandtotal=sales_total,diff=diff_amount,status="Short",totalpertype=gt,di=diamount,comment=comment,precoin=precoin,sales=sales_total)
            if record_Sales:
                record_Sales.save()
                CashierOrders.objects.filter(~Q(adminstatus=2),customer=customer_instance).update(adminstatus=2)
                Qadadic.objects.filter(customer=customer_instance,done=2).update(done=0)
                Sts.objects.filter(customer=customer_instance,done=2).update(done=0)
                Papers.objects.filter(customer=customer_instance,done=2).update(done=0)
                Notes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Swipes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Kazang.objects.filter(customer=customer_instance,done=2).update(done=0)
                Acc.objects.filter(customer=customer_instance,done=2).update(done=0)
                messages.info(request,f'Sale has been recorded successfully. Please hold for a few minutes while the process is completed in the background')
                return redirect('/sales_log')
        if sales_total < int(gt):
            record_Sales=Saleslog(cashier=customer_instance,grandtotal=sales_total,diff=diff_amount,status="Over",totalpertype=gt,di=diamount,comment=comment,precoin=precoin,sales=sales_total)
            if record_Sales:
                record_Sales.save()
                Qadadic.objects.filter(customer=customer_instance,done=2).update(done=0)
                Sts.objects.filter(customer=customer_instance,done=2).update(done=0)
                Papers.objects.filter(customer=customer_instance,done=2).update(done=0)
                Notes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Swipes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Kazang.objects.filter(customer=customer_instance,done=2).update(done=0)
                Acc.objects.filter(customer=customer_instance,done=2).update(done=0)
                CashierOrders.objects.filter(~Q(adminstatus=2),customer=customer_instance).update(adminstatus=2)
                messages.info(request,f'Sale has been recorded successfully. Please hold for a few minutes while the process is completed in the background')
                return redirect('/sales_log')
        if sales_total == int(gt):
            record_Sales=Saleslog(cashier=customer_instance,grandtotal=sales_total,diff=diff_amount,status="Balance",totalpertype=gt,di=diamount,comment=comment,precoin=precoin,sales=sales_total)
            if record_Sales:
                record_Sales.save()
                Qadadic.objects.filter(customer=customer_instance,done=2).update(done=0)
                Sts.objects.filter(customer=customer_instance,done=2).update(done=0)
                Papers.objects.filter(customer=customer_instance,done=2).update(done=0)
                Notes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Swipes.objects.filter(customer=customer_instance,done=2).update(done=0)
                Kazang.objects.filter(customer=customer_instance,done=2).update(done=0)
                Acc.objects.filter(customer=customer_instance,done=2).update(done=0)
                CashierOrders.objects.filter(~Q(adminstatus=2),customer=customer_instance).update(adminstatus=2)
                messages.info(request,f'Sale has been recorded successfully. Please hold for a few minutes while the process is completed in the background')
                return redirect('/sales_log')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def sales_logView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        return render(request,'supervisor/sales_log.html')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def filter_daily_reportView(request):
    if request.user.is_authenticated and request.user.is_supervisor and request.method=="POST":
        startdate =request.POST['startdate']
        enddate =request.POST['enddate']
        supervison_instance=request.user
        supervisor_username=supervison_instance.username 
        if not Saleslog.objects.filter(created_at__range=(startdate,enddate)):
                messages.info(request,f'No Data Found')
                return redirect('/sales_log')
        else:
            listof_permited_cashiers=User.objects.filter(is_activation=True,supervisor=supervisor_username).filter(is_cashier=True)
            sales_log=Saleslog.objects.filter(created_at__range=(startdate,enddate),cashier__in=listof_permited_cashiers)
            data = {
              'sales_log':sales_log,
              'startdate':startdate,
              'enddate':enddate
            }
            return render(request,'supervisor/sales_log.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def printView(request,from_date,end_date):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_authenticated and request.user.is_ceo:
        supervisor_instance = request.user 
        supervisor_username =supervisor_instance.username
        listof_permited_cashiers=User.objects.filter(is_activation=True,supervisor=supervisor_username).filter(is_cashier=True)
        sales_log=Saleslog.objects.filter(cashier__in=listof_permited_cashiers,created_at__range=(from_date,end_date)).order_by('-created_at')
        data = {
            'sales_log':sales_log,
            'from_date':from_date,
            'end_date':end_date,
        }
        return render(request,'print/print.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def print2View(request,cashier_id,startdate,enddate):
    if request.user.is_authenticated and request.user.is_supervisor or request.user.is_authenticated and request.user.is_ceo:
        cashier_instance=User.objects.get(id=cashier_id)
        processed_orders=CashierOrders.objects.filter(created_at__range=(startdate,enddate),adminstatus=2).filter(customer=cashier_instance)
        data={
         'processed_orders':processed_orders,
         'startdate':startdate,
         'enddate':enddate,
         'cashier_names':cashier_instance.first_name
        }
        return render(request,'print/print2.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def print_general_reportView(request,category,from_date,end_date):
    if request.user.is_authenticated and request.user.is_supervisor:
        supervisor_instance = request.user 
        supervisor_username =supervisor_instance.username
        listof_permited_cashiers=User.objects.filter(is_activation=True,supervisor=supervisor_username).filter(is_cashier=True)
        if category=="Qadadic":
            general_report_per_category=Qadadic.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Qadadic.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Sts":
            general_report_per_category=Sts.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Sts.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Papers":
            general_report_per_category=Papers.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Papers.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Notes":
            general_report_per_category=Notes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Notes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Kazang":
            general_report_per_category=Kazang.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Kazang.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Swipes":
            general_report_per_category=Swipes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Swipes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
        if category=="Acc":
            general_report_per_category=Acc.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Acc.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']
            }
            return render(request,'print/print3.html',context=data)
    else:
        return redirect('/')

    
@login_required(login_url='/')  
def general_reportView(request):
    if request.user.is_authenticated and request.user.is_supervisor:
        return render(request,'supervisor/general_report.html')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
def filter_general_reportView(request):
    if request.user.is_authenticated and request.user.is_supervisor and request.method=="POST":
        category =request.POST['type']
        from_date =request.POST['startdate']
        end_date =request.POST['enddate']
        supervison_instance=request.user
        supervisor_username=supervison_instance.username
        listof_permited_cashiers=User.objects.filter(is_activation=True,supervisor=supervisor_username).filter(is_cashier=True)
        if category == "Qadadic":
            general_report_per_category=Qadadic.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Qadadic.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Sts":
            general_report_per_category=Sts.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Sts.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Papers":
            general_report_per_category=Papers.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Papers.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Kazang":
            general_report_per_category=Kazang.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Kazang.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Swipes":
            general_report_per_category=Swipes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Swipes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Acc":
            general_report_per_category=Acc.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Acc.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
        if category == "Notes":
            general_report_per_category=Notes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).order_by('customer')[:20]
            data = {
                'general_report_per_category':general_report_per_category,
                'category':category,
                'from_date':from_date,
                'end_date':end_date,
                'grand_total':Notes.objects.filter(created_at__range=(from_date,end_date),status=1).filter(customer__in=listof_permited_cashiers).aggregate(Sum('amount'))['amount__sum']

            }
            return render(request,'supervisor/general_report.html',context=data)
    else:
        return redirect('/')