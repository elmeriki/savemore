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
from random_id import random_id
import string 

@login_required(login_url='/')  
def cashier_dashboardView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        qadadic_values = CashierOrders.objects.filter(customer=customer_instance,types="Qadadic")
        sts_values = CashierOrders.objects.filter(customer=customer_instance,types="Sts")
        notes_values=CashierOrders.objects.filter(customer=customer_instance,types="Note")
        papers_values=CashierOrders.objects.filter(customer=customer_instance,types="Papers")
        kazang_values=CashierOrders.objects.filter(customer=customer_instance,types="Kazang")
        swipes_values=CashierOrders.objects.filter(customer=customer_instance,types="Swipes")


        data  = {
        'qadadic_values':qadadic_values,
        'sts_values':sts_values,
        'notes_values':notes_values,
        'papers_values':papers_values,
        'kazang_values':kazang_values,
        'swipes_values':swipes_values,
        # 'sts_tota_sum':sts_tota_sum,
        # 'qadadic_tota_sum':qadadic_tota_sum,
        # 'note_tota_sum':note_tota_sum
        }
        return render(request,'cashier/cashier_dashboard.html',context=data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def add_qadadicView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        qadadic_list = Qadadic.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'qadadic_list':qadadic_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_qadadic.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_qadadicView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Qadadic.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Qadadic.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_qadadic/{cashierorderid}')
    else:
        return redirect('/')

@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_stsView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Sts.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Sts.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_sts/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_papersView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Papers.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Papers.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_paper/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_notesView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Notes.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Notes.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_notes/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_kazangView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Kazang.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Kazang.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_kazang/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/') 
@transaction.atomic  #transactional  
def delete_swipesView(request,cashierorderid,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        
        delete_amount = int(Swipes.objects.values_list('amount', flat=True).get(id=id))
        
        curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        new_amount = curent_Amount - delete_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_amount)
        Swipes.objects.filter(customer=customer_instance,id=id).delete()
        return redirect(f'/add_swipes/{cashierorderid}')
    else:
        return redirect('/')


@login_required(login_url='/')  
def add_qadadic_listView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        qadadic_orders = CashierOrders.objects.filter(customer=customer_instance,types="Qadadic").order_by('-created_at')
        data = {
        'qadadic_orders':qadadic_orders
        }
        return render(request,'cashier/qadadic_list.html',context=data)
    else:
        return redirect('/add_qadadic_list')

@login_required(login_url='/')  
def add_stsView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        sts_list = Sts.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'sts_list':sts_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_sts.html',context=data)
    else:
        return redirect('/')


@login_required(login_url='/')  
def add_notesView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        notes_list = Notes.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'notes_list':notes_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_notes.html',context=data)
    else:
        return redirect('/')


@login_required(login_url='/')  
def add_kazangView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        kazang_list = Kazang.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'kazang_list':kazang_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_kazang.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def add_wipesView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        swipes_list = Swipes.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'swipes_list':swipes_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_swipes.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def papers_listView(request):
    username=request.user.username
    customer_instance =User.objects.get(username=username)
    paper_values_list = CashierOrders.objects.filter(customer=customer_instance,types="Papers").order_by('-created_at')
    if paper_values_list: 
        data = {
        'paper_values_list':paper_values_list
        }
        return render(request,'cashier/paper_list.html',context=data)
    else:
        return render(request,'cashier/paper_list.html',{})

@login_required(login_url='/')  
def kazang_listView(request):
    username=request.user.username
    customer_instance =User.objects.get(username=username)
    kazang_values_list = CashierOrders.objects.filter(customer=customer_instance,types="Kazang").order_by('-created_at')
    if kazang_values_list: 
        data = {
        'kazang_values_list':kazang_values_list
        }
        return render(request,'cashier/kazang_list.html',context=data)
    else:
        return render(request,'cashier/kazang_list.html',{})


@login_required(login_url='/')  
def swipe_listView(request):
    username=request.user.username
    customer_instance =User.objects.get(username=username)
    swipes_values_list = CashierOrders.objects.filter(customer=customer_instance,types="Swipes").order_by('-created_at')
    if swipes_values_list: 
        data = {
        'swipes_values_list':swipes_values_list
        }
        return render(request,'cashier/swipes_list.html',context=data)
    else:
        return render(request,'cashier/swipes_list.html',{})

@login_required(login_url='/')  
def save_paperView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        bookno = request.POST['bookno']
        amount = int(request.POST['amount'])
        booknoleng = len(str(bookno))
        if booknoleng < 4 or booknoleng > 4:
            messages.info(request,'Book Number must 4 Numbers')
            return redirect(f'/add_paper/{id}')
        if booknoleng == 4:
            save_papers_values=Papers(customer=customer_instance,bookno=bookno,amount=amount,cashierorid=id)
            if save_papers_values:
                save_papers_values.save()
                curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
                new_amount = curent_Amount + amount
                CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
                return redirect(f'/add_paper/{id}')
            else:
                return redirect('/')
    else:
        return redirect('/')
        

@login_required(login_url='/')  
def add_paperView(request,id):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        paper_list =Papers.objects.filter(customer=customer_instance,cashierorid=id)
        admin_status=int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'paper_list':paper_list,
        'admin_status':admin_status
        }
        return render(request,'cashier/add_paper.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def notes_listView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        notes_values_list=CashierOrders.objects.filter(customer=customer_instance,types="Note").order_by('-created_at')
        if notes_values_list: 
            data = {
            'notes_values_list':notes_values_list
            }
            return render(request,'cashier/notes_list.html',context=data)
        else:
            return render(request,'cashier/notes_list.html')
    else:
        return redirect('/notes_list')
    

@login_required(login_url='/')  
def cashier_reviewView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance=User.objects.get(username=username)
        cashier_review = Saleslog.objects.filter(cashier=customer_instance)
        data = {
        'cashier_review':cashier_review
        }
        return render(request,'cashier/cashier_reviews.html',context=data)
    else:
        return redirect('/')


@login_required(login_url='/')  
def sts_listView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        sts_values_list = CashierOrders.objects.filter(customer=customer_instance,types="Sts").order_by('-created_at')
        if sts_values_list: 
            data = {
            'sts_values_list':sts_values_list
            }
            return render(request,'cashier/sts_list.html',context=data)
        else:
            return render(request,'cashier/sts_list.html')
    else:
        return redirect('/sts_list')
        
@login_required(login_url='/')  
def confirm_creating_orderView(request,type):
    if request.user.is_authenticated and request.user.is_cashier:
        data = {
        'type':type
        }
        return render(request,'cashier/confirmation.html',context=data)

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def new_cashier_orderView(request,type):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        import random
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        
        if CashierOrders.objects.filter(customer=customer_instance,types=type).filter(created_at__gt=date_from):
            messages.info(request,f'You are authorise to create a new {type} in 24 hours.')
            return redirect(f'/confirm_creating_order/{type}')
        
        cashoutid = random_id(length=8,character_set=string.digits)
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Qadadic":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/add_qadadic_list')
        
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Sts":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/sts_list')
        
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Papers":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/papers_list')
        
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Note":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/notes_list')
        
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Kazang":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/kazang_list')
        
        if not CashierOrders.objects.filter(customer=customer_instance,status=0).filter(cashierorid=cashoutid) and type=="Swipes":
            save_cashout_id = CashierOrders(customer=customer_instance,cashierorid=cashoutid,types=type)
            save_cashout_id.save()
            return redirect('/swipe_list')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_qadadicView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        bookno = int(request.POST['bookno'])
        amount = int(request.POST['amount'])
        booknoleng = len(str(bookno))
        if booknoleng < 4 or booknoleng > 4:
            messages.info(request,'Book Number must 4 Numbers')
            return redirect(f'/add_qadadic/{id}')
        if booknoleng == 4:
            save_qadadic_values =Qadadic(customer=customer_instance,bookno=bookno,amount=amount,cashierorid=id)
            if save_qadadic_values:
                save_qadadic_values.save()
                curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
                new_amount = curent_Amount + amount
                CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
                return redirect(f'/add_qadadic/{id}')
            else:
                return redirect('/')
    else:
        return redirect('/')
    
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_stsView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        bookno = request.POST['bookno']
        amount = int(request.POST['amount'])
        booknoleng = len(str(bookno))
        if booknoleng < 4 or booknoleng > 4:
            messages.info(request,'Book Number must 4 Numbers')
            return redirect(f'/add_sts/{id}')
        if booknoleng == 4:
            save_sts_values=Sts(customer=customer_instance,bookno=bookno,amount=amount,cashierorid=id)
            if save_sts_values:
                save_sts_values.save()
                curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
                new_amount = curent_Amount + amount
                CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
                return redirect(f'/add_sts/{id}')
            else:
                return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_kazangView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        amount = int(request.POST['amount'])
        save_kazang_values=Kazang(customer=customer_instance,amount=amount,cashierorid=id)
        if save_kazang_values:
            save_kazang_values.save()
            curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
            new_amount = curent_Amount + amount
            CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
            return redirect(f'/add_kazang/{id}')
        else:
            return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_notesView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        amount = int(request.POST['amount'])
        save_notes_values=Notes(customer=customer_instance,amount=amount,cashierorid=id)
        if save_notes_values:
            save_notes_values.save()
            curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
            new_amount = curent_Amount + amount
            CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
            return redirect(f'/add_notes/{id}')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def save_add_swipesView(request,id):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        amount = int(request.POST['amount'])
        save_swipes_values=Swipes(customer=customer_instance,amount=amount,cashierorid=id)
        if save_swipes_values:
            save_swipes_values.save()
            curent_Amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=id))
            new_amount = curent_Amount + amount
            CashierOrders.objects.filter(customer=customer_instance,cashierorid=id).update(amount=new_amount)
            return redirect(f'/add_swipes/{id}')
        else:
            return redirect('/')
    else:
        return redirect('/')
    

@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_qadadicView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        qadadic_list = Qadadic.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Qadadic.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'qadadic_list':qadadic_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_qadadic.html',context=data)
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_stsView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        sts_list = Sts.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Sts.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'sts_list':sts_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_sts.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_papersView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        paper_list = Papers.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Papers.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'paper_list':paper_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_papers.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_notesView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        notes_list = Notes.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Notes.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'notes_list':notes_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_notes.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_kazangView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        kazang_list = Kazang.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Kazang.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'kazang_list':kazang_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_kazang.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_swipesView(request,id,pk):
    if request.user.is_authenticated and request.user.is_cashier:
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        swipes_list = Swipes.objects.filter(customer=customer_instance,cashierorid=id)
        single_update = Swipes.objects.filter(customer=customer_instance,id=pk)
        admin_status = int(CashierOrders.objects.values_list('adminstatus', flat=True).get(cashierorid=id))
        data={
        'id':id,
        'swipes_list':swipes_list,
        'admin_status':admin_status,
        'single_update':single_update
        }
        return render(request,'cashier/edith_swipes.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_qadadicView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        bookno = request.POST['bookno']
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Qadadic.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Qadadic.objects.filter(id=id).update(amount=form_amount)
        Qadadic.objects.filter(id=id).update(bookno=bookno)
        return redirect(f'/add_qadadic/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_stsView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        bookno = request.POST['bookno']
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Sts.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Sts.objects.filter(id=id).update(amount=form_amount)
        Sts.objects.filter(id=id).update(bookno=bookno)
        
        return redirect(f'/add_sts/{cashierorderid}')
    else:
        return redirect('/')
    
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_papersView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        bookno = request.POST['bookno']
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Papers.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Papers.objects.filter(id=id).update(amount=form_amount)
        Papers.objects.filter(id=id).update(bookno=bookno)
        return redirect(f'/add_paper/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_notesView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Notes.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Notes.objects.filter(id=id).update(amount=form_amount)
        return redirect(f'/add_notes/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_kazangView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Kazang.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Kazang.objects.filter(id=id).update(amount=form_amount)
        return redirect(f'/add_kazang/{cashierorderid}')
    else:
        return redirect('/')
    
@login_required(login_url='/')  
@transaction.atomic  #transactional 
def update_add_swipesView(request,id,cashierorderid):
    if request.user.is_authenticated and request.user.is_cashier and request.method=="POST":
        form_amount = int(request.POST['amount'])
        username=request.user.username
        customer_instance =User.objects.get(username=username)
        total_amount = int(CashierOrders.objects.values_list('amount', flat=True).get(cashierorid=cashierorderid))
        curent_amount = int(Swipes.objects.values_list('amount', flat=True).get(id=id))
        new_amount=total_amount - curent_amount
        new_new_amount = new_amount + form_amount
        CashierOrders.objects.filter(customer=customer_instance,cashierorid=cashierorderid).update(amount=new_new_amount)
        Swipes.objects.filter(id=id).update(amount=form_amount)
        return redirect(f'/add_swipes/{cashierorderid}')
    else:
        return redirect('/')