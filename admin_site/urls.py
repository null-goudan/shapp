from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('welcome/', views.welcome),
    path('table_user/', views.table_user),
    path('table_doing/', views.table_doing),
    path('table_finish/', views.table_finish),
    path('table_waiting/', views.table_waiting),
    path('update_user/', views.update_user),
    path('delete_user/', views.delete_user),
    path('user-setting', views.user_setting),
    path('user-password', views.user_password),
    path('editor/', views.editor),
    path('user_search/', views.user_search),

]