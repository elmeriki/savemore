from django.urls import path,include
from superadmin import views

urlpatterns = [
    path('cashier_permision/<str:userid>', views.cashier_permisionView, name='cashier_permisionView'),
    path('save_cashier_permision/<str:userid>', views.save_cashier_permisionView, name='save_cashier_permisionView'),
    path('delete_cashier_permission/<str:userid>/<str:types>', views.delete_cashier_permissionView, name='delete_cashier_permissionView'),
    path('approve_account', views.approve_accountView, name='approve_accountView'),
    path('activate_account/<int:id>', views.approved_accountView, name='approved_accountView'),
    path('activate_supervisor_account/<int:id>', views.activate_supervisor_accountView, name='activate_supervisor_accountView'),
    path('diactivate_account/<int:id>', views.diactivate_accountView, name='diactivate_accountView'),
    path('diactivate_supervisor_account/<int:id>', views.diactivate_supervisor_accountView, name='diactivate_supervisor_accountView'),
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
    path('admin_edith_order_detail/<int:order_id>', views.admin_edith_order_detailView, name='admin_edith_order_detailView'),
    path('admin_update_order_detail/<int:id>/<int:qty>/<int:orderid>', views.admin_update_order_detailView, name='admin_update_order_detailView'),
    path('supervisors', views.supervisorsView, name='supervisorsView'),
    path('cashier_order', views.cashier_orderView, name='cashier_orderView'),
    path('delete_cashier_order/<int:cashierorid>', views.delete_cashier_orderView, name='delete_cashier_orderView'),
    path('supervisor_permision/<str:userid>', views.supervisor_permisionView, name='supervisor_permisionView'),
    path('save_supervisor_permision/<str:userid>', views.save_supervisor_permisionView, name='save_supervisor_permisionView'),
    path('delete_supervisor_permission/<str:userid>/<str:supervisorid>', views.delete_supervisor_permissionView, name='delete_supervisor_permissionView'),
]
