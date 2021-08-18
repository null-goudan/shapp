from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log),
    path('reg/', views.reg),
    path('add/', views.add),
]
