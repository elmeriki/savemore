from django.urls import path,include
from supervisor import views

urlpatterns = [
    path('supervisor_dashboard', views.supervisor_dashboardView, name='supervisor_dashboardView'),
    path('supervisor_profile', views.supervisor_profileView, name='supervisor_profileView'),
    path('single_cashier/<int:userid>', views.single_cashierView, name='single_cashierView'),
    path('single_cashier_ceo/<int:userid>', views.single_cashier_ceoView, name='single_cashier_ceoView'),
    path('process_actual/<str:orderid>/<str:type>/<str:customerid>', views.process_actualView, name='process_actualView'),
    path('process_actual_save/<str:orderid>/<str:type>/<str:customerid>', views.process_actual_saveView, name='process_actual_saveView'),
    path('processed_log', views.processed_logView, name='processed_logView'),
    path('search_processed_log', views.search_processed_logView, name='search_processed_logView'),
    path('processed_sales', views.processed_salesView, name='processed_salesView'),
    path('single_processed_sales/<int:userid>', views.single_processed_salesView, name='single_processed_salesView'),

    path('view_single_processed_order/<str:cashierorid>>', views.view_single_processed_orderView, name='view_single_processed_orderView'),
    path('processed_single_order/<int:cashierorid>/<str:types>', views.processed_single_orderView, name='processed_single_orderView'),
    path('processed_qadadic/<int:cashierorid>/<str:type>', views.processed_qadadicView, name='processed_qadadicView'),
    path('record_sales/<int:userid>/<int:grand_total>', views.record_salesView, name='record_salesView'),
    path('record_salessave/<int:userid>/<int:gt>', views.record_salessaveView, name='record_salessaveView'),
    path('sales_log', views.sales_logView, name='sales_logView'),
    path('filter_daily_report', views.filter_daily_reportView, name='filter_daily_reportView'),
    path('print', views.printView, name='printView'),
    path('print2/<str:startdate>/<str:enddate>/<str:cashier_id>', views.print2View, name='print2View'),
    
    path('print_general_report/<str:from_date>/<str:end_date>/<str:category>', views.print_general_reportView, name='print_general_reportView'),

    path('general_report', views.general_reportView, name='general_reportView'),
    path('filter_general_report', views.filter_general_reportView, name='filter_general_reportView'),

]
