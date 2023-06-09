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
import threading

class Emailthread(threading.Thread):
    def __init__(self,msg):
        self.msg=msg
        threading.Thread.__init__(self)
    def run(self):
        self.msg.send(fail_silently=False)
        

def landPageView(request):
    if request.user.is_authenticated and request.user.is_cashier:
        return redirect('/cashier_dashboard')
    
    if request.user.is_authenticated and request.user.is_cashier:
        return redirect('/cashier_dashboard')
    
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('/super_admin_dashboard')
    
    if request.user.is_authenticated and request.user.is_customer:
        return redirect('/customer_dashboard')
    
    else:
        return render(request,'customer/login.html',{})


def createAccountView(request):
    return render(request,'customer/register.html',{})

@login_required(login_url='/')  
def customer_profileView(request):
    if request.user.is_authenticated and request.user.is_customer:
        return render(request,'customer/customer_profile.html',{})
    else:
        return redirect('/')
    
def super_admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_admin:
        customer_orders = Order.objects.all()[:5]
        customer_list = User.objects.filter(is_customer=True).order_by('-date_joined')[:10]
        order_list = Order.objects.all().order_by('-created_at')[:10]
        order_count_total =Order.objects.all().count()
        invoice_count_total =Order.objects.filter(adminstatus=1).count()
        paid_count_total =Order.objects.filter(adminstatus=4).count()
        data = {
        'customer_orders':customer_orders,
        'customer_list':customer_list,
        'order_list':order_list,
        'order_count_total':order_count_total,
        'invoice_count_total':invoice_count_total,
        'paid_count_total':paid_count_total
        }
        return render(request,'customer/admin_dashboard.html',context=data)
    
    else:
        return redirect('/')
    

@login_required(login_url='/')  
def admin_dashboardView(request):
    if request.user.is_authenticated and request.user.is_ceo:
        order_count_total =Order.objects.all().count()
        invoice_count_total =Order.objects.filter(adminstatus=1).count()
        paid_count_total =Order.objects.filter(adminstatus=4).count()
        all_customers =User.objects.filter(is_customer=True).exclude(is_superuser=True)
        sales_log=Saleslog.objects.all().order_by('-created_at')[:10]
        data = {
        'order_count_total':order_count_total,
        'invoice_count_total':invoice_count_total,
        'paid_count_total':paid_count_total,
        'all_customers':all_customers,
        'sales_log':sales_log
        }
        return render(request,'customer/ceo_dashboard.html',context=data)
    else:
        return redirect('/')

@login_required(login_url='/')  
def fetch_sales_logView(request):
    if request.user.is_authenticated and request.user.is_ceo:
        sales_log=Saleslog.objects.all().order_by('-created_at')[:10]
        data = {
        'sales_log':sales_log
        }
        return render(request,'customer/sales_log.html',context=data)
    else:
        return redirect('/')
    
@login_required(login_url='/')  
def fetch_sales_log_cashierView(request,selected_date):
    if request.user.is_authenticated and request.user.is_ceo:
        cashier_list =CashierOrders.objects.filter(created_at=selected_date)
        data  = {
        'cashier_list':cashier_list
        }
        return render(request,'customer/sales_fetch_data.html',context=data)
    
@login_required(login_url='/')  
def admin_profileView(request):
    if request.user.is_authenticated and request.user.is_ceo:
        return render(request,'customer/ceo_profile.html',{})
    else:
        return redirect('/')

@login_required(login_url='/')  
def customer_dashboardView(request):
    if request.user.is_authenticated and request.user.is_customer:
        username =request.user.username 
        customer_instance = User.objects.get(username=username)
        promo_messages=Promotion.objects.filter(customer=customer_instance,status=0).order_by('-created_at')[:5]
        order_list = Order.objects.filter(customer=customer_instance).order_by('-created_at')[:5]
        order_count_total =Order.objects.filter(customer=customer_instance).count()
        invoice_count_total =Order.objects.filter(customer=customer_instance,adminstatus=1).count()
        paid_count_total =Order.objects.filter(customer=customer_instance,adminstatus=4).count()

        data ={
            'order_list':order_list,
            'order_count_total':order_count_total,
            'promo_messages':promo_messages,
            'invoice_count_total':invoice_count_total,
            'paid_count_total':paid_count_total
        }
        return render(request,'customer/customer_dashboard.html',context=data)
    else:
        return redirect('/')


def createAccountManagementView(request):
    return render(request,'customer/reg_management.html',{})

@transaction.atomic
def create_new_accountView(request):
    if request.method =="POST" and request.POST['businessname'] and request.POST['subburb'] and  request.POST['city'] and request.POST['businessaddress'] and request.POST['fullnames'] and request.POST['email'] and request.POST['cellphone'] and request.POST['password']:
        businessname = request.POST['businessname']
        subburb = request.POST['subburb']
        city = request.POST['city']
        fullnames = request.POST['fullnames']
        email = request.POST['email']
        cellphone = request.POST['cellphone']
        password = request.POST['password']
        businessaddress = request.POST['businessaddress']
                
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email has been taken already.')
            return redirect('/register')  
        
        if User.objects.filter(username=cellphone).exists():
            messages.info(request,'Cellphone has been taken already.')
            return redirect('/register')  
        
        create_new_customer_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_customer=True,email=email,shopname=businessname,shopaddress=businessaddress,city=city,is_activation=True,subburb=subburb)
        if create_new_customer_account:
            create_new_customer_account.save()

            subject = 'Welcome to Savemore Groups'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'''<p><strong>Dear {fullnames} </strong> <br><br>  This email serves to confirm that your savaMore Groups account has been created successfully, 
            Login and starting placing orders at the confort of your sofas.
            <br> <strong>Login Credentials:</strong><br> 
            Username:{cellphone} <br> Password: {password} <br><br> 
            Our Mission: Making Online Shopping Convenient and Flexible for SaveMore Customers. 
            <br><hr> Best Regards <br> SaveMore Group </p>'''
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        return render(request,'customer/reg_management.html',{})
    else:
        return redirect('/register')  
    
@transaction.atomic
def customer_loginView(request):
    if request.method =="POST" and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password =request.POST['password']
                
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Incorrect credentials.')
            return redirect('/')  
        
        userlog = auth.authenticate(username=username,password=password)
        # checking if it is an existing user in the database
        
        # customise error messages handler
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_customer:
                return redirect('/customer_dashboard')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
                
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and not request.user.is_activation:
                messages.info(request,"Account is not yet activated")
                return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_ceo:
                return redirect('/admin_dashboard')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_admin:
                return redirect('/super_admin_dashboard')
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_cashier:
                return redirect('/cashier_dashboard')
            
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_supervisor:
                return redirect('/supervisor_dashboard')
            
        else:
            messages.info(request,"Incorrect credentials.")
            return redirect('/')
    else:
        return redirect('/')  
    
    
def logoutView(request):
    auth.logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('/') 

# def lognotauthorise(request):
#     auth.logout(request)
#     messages.info(request,"You are not authorise to login here")
#     return redirect('/school_log') 


@transaction.atomic
def create_new_manage_accountView(request):
    if request.method =="POST" and request.POST['branch'] and request.POST['decination'] and request.POST['fullnames'] and request.POST['email'] and request.POST['cellphone'] and request.POST['password']:
        decination = request.POST['decination']
        branch = request.POST['branch']
        fullnames = request.POST['fullnames']
        email = request.POST['email']
        cellphone = request.POST['cellphone']
        password = request.POST['password']
        
        if branch == "":
            messages.info(request,'Select a branch')
            return redirect('/reg_management') 
        
        if decination == "":
            messages.info(request,'Select a decination')
            return redirect('/reg_management') 
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email has been used already.')
            return redirect('/reg_management')  
        
        if User.objects.filter(username=cellphone).exists():
            messages.info(request,'Cellphone has been used already.')
            return redirect('/reg_management')  
        
        if decination == "1":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_ceo=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Administrator Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (CEO) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        if decination == "2":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_admin=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Administrator Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (Administrator) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        if decination == "3":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_marketer=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Administrator Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (Marketing) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        if decination == "4":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_cashier=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Administrator Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (Cashier) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        if decination == "5":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_stock=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Administrator Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (Stock Management) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        if decination == "6":
            create_new_admin_account = User.objects.create_user(username=cellphone,first_name=fullnames,last_name=fullnames,password=password,is_supervisor=True,email=email,branch=branch)
            create_new_admin_account.save()
            #admin email notications for creating new account
            subject = 'New Supervisor Profile'
            from_email='SaveMore Groups <no_reply@savemoregroup.com>'
            sento = email
            messagbody = '#'
            html_content =f'<p><strong>Dear {fullnames} (Supervisor) </strong> <br><br>  This email serves to confirm that your account has been created successfully, You can only login once your account is activated.<br> Login Credentials:<br> Username:{cellphone} <br> Password: {password} <br><br> Our mission is to provide saveMore Groups customers with an easy and accurate means of placing orders online at the confort of their Home. <br><hr> Best Regards <br> SaveMore Group </p>'
            msg=EmailMultiAlternatives(subject, messagbody, from_email,[sento])
            msg.attach_alternative(html_content, "text/html")
            Emailthread(msg).start()
            messages.info(request,'Account Created Successfully')
            return redirect('/')  
        return render(request,'customer/reg_management.html',{})
    else:
        return redirect('/register')  