from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log),
    path('houtai_login/', views.houtai_log),
    path('reg/', views.reg),
    path('take/', views.add_take),
    path('buy/', views.add_buy),
    path('do/', views.add_do),
    path('information/', views.infomation),
    path('information/get/',views.information_userinfo),
    path('password/', views.password),
    path('send/', views.send),
    path('send_table_info/', views.send_table_info),
    path('help/', views.help),
    path('order/', views.order),
    path('get_list/', views.get_list),
    path('delete/', views.del_table),
    path('finished/', views.finish_table),
    path('table_update/', views.update),
    path('order_list/', views.order_list),
]
