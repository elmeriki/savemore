from django.urls import path,include
from cashiers import views

urlpatterns = [
    path('cashier_dashboard', views.cashier_dashboardView, name='cashier_dashboardView'),
    path('add_qadadic_list', views.add_qadadic_listView, name='add_qadadic_listView'),
    path('add_qadadic/<str:id>', views.add_qadadicView, name='add_qadadicView'),
    path('delete_qadadic/<str:cashierorderid>/<str:id>', views.delete_qadadicView, name='delete_qadadicView'),
    path('delete_sts/<str:cashierorderid>/<str:id>', views.delete_stsView, name='delete_stsView'),
    path('delete_papers/<str:cashierorderid>/<str:id>', views.delete_papersView, name='delete_papersView'),
    path('delete_notes/<str:cashierorderid>/<str:id>', views.delete_notesView, name='delete_notesView'),
    path('delete_kazang/<str:cashierorderid>/<str:id>', views.delete_kazangView, name='delete_kazangView'),
    path('delete_acc/<str:cashierorderid>/<str:id>', views.delete_accView, name='delete_accView'),
    path('delete_swipes/<str:cashierorderid>/<str:id>', views.delete_swipesView, name='delete_swipesView'),
    path('save_add_qadadic/<str:id>', views.save_add_qadadicView, name='save_add_qadadicView'),
    path('add_sts/<str:id>', views.add_stsView, name='add_stsView'),
    path('sts_list', views.sts_listView, name='sts_listView'),
    path('kazang_list', views.kazang_listView, name='kazang_listView'),
    path('swipe_list', views.swipe_listView, name='swipe_listView'),
    path('acc_list', views.acc_listView, name='acc_listView'),

    path('cashier_review', views.cashier_reviewView, name='cashier_reviewView'),

    path('cashiers_profile', views.cashiers_profileView, name='cashiers_profileView'),
    path('ceo_profile', views.ceo_profileView, name='ceo_profileView'),


    path('update_add_qadadic/<str:id>/<str:cashierorderid>', views.update_add_qadadicView, name='update_add_qadadicView'),
    path('update_add_sts/<str:id>/<str:cashierorderid>', views.update_add_stsView, name='update_add_stsView'),
    path('update_qadadic/<str:id>/<str:pk>', views.update_qadadicView, name='update_qadadicView'),
    path('update_sts/<str:id>/<str:pk>', views.update_stsView, name='update_stsView'),

    path('update_papers/<str:id>/<str:pk>', views.update_papersView, name='update_papersView'),
    path('update_add_papers/<str:id>/<str:cashierorderid>', views.update_add_papersView, name='update_add_papersView'),
    
    path('update_notes/<str:id>/<str:pk>', views.update_notesView, name='update_notesView'),
    path('update_add_notes/<str:id>/<str:cashierorderid>', views.update_add_notesView, name='update_add_notesView'),
    
    path('update_kazang/<str:id>/<str:pk>', views.update_kazangView, name='update_kazangView'),
    
    path('update_acc/<str:id>/<str:pk>', views.update_accView, name='update_accView'),

    path('update_add_kazang/<str:id>/<int:cashierorderid>', views.update_add_kazangView, name='update_add_kazangView'),
    
    path('update_swipes/<str:id>/<str:pk>', views.update_swipesView, name='update_swipesView'),
    path('update_add_swipes/<str:id>/<int:cashierorderid>', views.update_add_swipesView, name='update_add_swipesView'),

    path('save_add_sts/<str:id>', views.save_add_stsView, name='save_add_stsView'),
    path('add_notes/<str:id>', views.add_notesView, name='add_notesView'),
    path('add_kazang/<str:id>', views.add_kazangView, name='add_kazangView'),
    
    path('add_acc/<str:id>', views.add_accView, name='add_accView'),
    
    path('add_swipes/<str:id>', views.add_wipesView, name='add_wipesView'),
    path('save_add_swipes/<str:id>', views.save_add_swipesView, name='save_add_swipesView'),
    path('save_add_notes/<str:id>', views.save_add_notesView, name='save_add_notesView'),
    path('save_add_kazang/<str:id>', views.save_add_kazangView, name='save_add_kazangView'),
    path('save_add_acc/<str:id>', views.save_add_accView, name='save_add_accView'),
    path('notes_list', views.notes_listView, name='notes_listView'),
    path('papers_list', views.papers_listView, name='papers_listView'),
    path('add_paper/<str:id>', views.add_paperView, name='add_paperView'),
    path('save_paper/<str:id>', views.save_paperView, name='save_paperView'),
    path('confirm_creating_order/<str:type>', views.confirm_creating_orderView, name='confirm_creating_orderView'),
    path('new_cashier_order/<str:type>', views.new_cashier_orderView, name='new_cashier_orderView'),
]
