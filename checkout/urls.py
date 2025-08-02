from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:order_number>/', views.checkout, name='checkout'),
]
