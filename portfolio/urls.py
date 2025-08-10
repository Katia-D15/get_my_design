from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio_items, name="portfolio_items"),
]
