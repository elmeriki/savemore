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
    path('admin_chat_reply/<int:chatid>', views.admin_chat_replyView, name='admin_chat_replyView'),
    path('admin_response_message/<int:chatid>', views.admin_response_messageView, name='admin_response_messageView'),
    path('expenses_filter', views.expenses_filterView, name='expenses_filterView'),
    path('dialysales_filter', views.dialysales_filterView, name='dialysales_filterView'),
    path('fetch_daily_Sales', views.fetch_daily_SalesView, name='fetch_daily_SalesView'),
    path('fetch_daily_expenses', views.fetch_daily_expensesView, name='fetch_daily_expensesView'),
    path('search_customers', views.search_customersView, name='search_customersView'),
    path('customer_search', views.customer_searchView, name='customer_searchView'),

]
