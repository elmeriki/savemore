from django.urls import path,include
from cashiers import views

urlpatterns = [
    path('cashier_dashboard', views.cashier_dashboardView, name='cashier_dashboardView'),
]
