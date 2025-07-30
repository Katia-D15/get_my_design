from django.urls import path
from . import views

urlpatterns = [
    path("order", views.create_order, name="create_order"),
    path("review", views.review_order, name="review_order"),
]
