from django.urls import path,include
from superadmin import views

urlpatterns = [
    path('approve_account', views.approve_accountView, name='approve_accountView'),
    path('activate_account/<int:id>', views.approved_accountView, name='approved_accountView'),
    path('promotion', views.promotionView, name='promotionView'),
    path('send_promo', views.send_promoView, name='send_promoView'),
    path('send_to_all_customer_promo', views.send_to_all_customer_promoView, name='send_to_all_customer_promoView'),
    path('expenses_display', views.expenses_displayView, name='expenses_displayView'),
    path('dailysales_display', views.dailysales_displayView, name='dailysales_displayView'),
    path('expenses', views.expensesView, name='expensesView'),
    path('dailysales', views.dailysalesView, name='dailysalesView'),
    path('save_daily_expenses', views.save_daily_expensesView, name='save_daily_expensesView'),
    path('save_daily_sales', views.save_daily_SalesView, name='save_daily_SalesView'),
    path('search_product', views.search_productView, name='search_productView'),
    path('add_to_cart/<int:id>', views.add_to_cartView, name='add_to_cartView'),
    path('admin_order_list', views.admin_order_listView, name='admin_order_listView'),
    path('admin_order_detail/<int:order_id>', views.admin_order_detailView, name='admin_order_detailView'),
    path('process_order/<int:order_id>', views.process_orderView, name='process_orderView'),
    path('update_order_status', views.update_order_statusView, name='update_order_statusView'),
    path('chat_room', views.chat_roomView, name='chat_roomView'),
]
