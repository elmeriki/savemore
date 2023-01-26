from django.urls import path,include
from stock import views

urlpatterns = [
    path('stock', views.stock_import_View, name='stock_import_View'),

]
