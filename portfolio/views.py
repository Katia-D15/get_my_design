from django.shortcuts import render
from .models import PortfolioItem
from core.choices import DesignTypeChoices


def portfolio_items(request):
    """
    Display a list of visible portfolio items,
    optionally filtered by design type.
    """
    selected_type = request.GET.get('design_type', '')

    items = PortfolioItem.objects.filter(visible=True).only(
        'title', 'design_type', 'image', 'description').order_by('-created_at')

    if selected_type:
        items = items.filter(design_type=selected_type)

    context = {'items': items,
               'selected_type': selected_type,
               'available_types': DesignTypeChoices.choices,
               }
    return render(request, 'portfolio/portfolio_items.html', context)
