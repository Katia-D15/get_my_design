from django.urls import path
from . import views

urlpatterns = [
    path("order", views.create_order, name="create_order"),
    path(
        "review/<str:order_number>/",
        views.review_order,
        name="review_order"),
    path("", views.my_orders, name="my_orders"),
]
