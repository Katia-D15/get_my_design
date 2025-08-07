from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('wh/', webhook, name='webhook'),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'),
    path(
        'checkout_success/<str:order_number>/',
        views.checkout_success,
        name='checkout_success'),
    path('<str:order_number>/', views.checkout, name='checkout'),

]
