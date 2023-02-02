from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('savemauth.urls')),
    path('', include('stock.urls')),
    path('', include('customer.urls')),
    path('', include('superadmin.urls')),
    path('', include('cashiers.urls')),
]
