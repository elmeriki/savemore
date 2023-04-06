from django.urls import path,include
from savemauth import views
urlpatterns = [
    
    path('', views.landPageView, name='landPageView'),
    path('register', views.createAccountView, name='createAccountView'),
    path('create_new_account', views.create_new_accountView, name='create_new_accountView'),
    path('create_new_manage_account', views.create_new_manage_accountView, name='create_new_manage_accountView'),
    path('reg_management', views.createAccountManagementView, name='createAccountManagementView'),
    path('customer_login', views.customer_loginView, name='customer_loginView'),
    path('customer_dashboard', views.customer_dashboardView, name='customer_dashboardView'),
    path('customer_profile', views.customer_profileView, name='customer_profileView'),
    path('admin_profile', views.admin_profileView, name='admin_profileView'),
    path('admin_dashboard', views.admin_dashboardView, name='admin_dashboardView'),
    path('logout', views.logoutView, name='logoutView'),
    path('super_admin_dashboard', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('fetch_sales_log', views.fetch_sales_logView, name='fetch_sales_logView'),
    path('fetch_sales_log_cashier/<str:selected_date>', views.fetch_sales_log_cashierView, name='fetch_sales_log_cashierView'),

]
