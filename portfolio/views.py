from django.shortcuts import render
from .models import PortfolioItem


def portfolio_items(request):
    return render(request, 'portfolio/portfolio_items.html',)
