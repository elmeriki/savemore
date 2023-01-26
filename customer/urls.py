from django.urls import path,include
from customer import views

urlpatterns = [
    path('new_order', views.new_orderView, name='new_orderView'),
    path('invoice', views.invoiceView, name='invoiceView'),
    path('conversation', views.conversationView, name='conversationView'),
    path('list_customers', views.list_customersView, name='list_customersView'),
    path('order_list', views.order_listView, name='order_listView'),
    path('customer_promo_message', views.customer_promo_messageView, name='customer_promo_messageView'),
    path('order_detail/<int:order_id>', views.order_detailView, name='order_detailView'),
    path('delete_single_order/<int:order_id>/<int:id>', views.delete_single_orderView, name='delete_single_orderView'),
    path('update_quantity/<int:order_id>/<int:id>', views.update_quantityView, name='update_quantityView'),
    path('update_quantity/<int:order_id>/<int:id>', views.update_quantityView, name='update_quantityView'),
    path('update_order_status/<int:order_id>', views.update_order_statusView, name='update_order_statusView'),
    path('chat_message', views.chat_messageView, name='chat_messageView'),
    path('delete_chat_message/<int:id>', views.delete_chat_messageView, name='delete_chat_messageView'),
    path('track_order', views.track_orderView, name='track_orderView'),
    path('track_my_order', views.track_my_orderView, name='track_my_orderView'),
    path('message_detail', views.message_detailView, name='message_detailView'),

]
