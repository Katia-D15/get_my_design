from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm


@login_required
def create_order(request):
    '''
    Create an order with status pending
    '''
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'pending'
            order.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your order was saved successfully'
                                 )
            return render(
                request, 'orders/order_review.html', {'order': order}
                )
    else:
        form = OrderForm()

    return render(request, 'orders/request_your_design.html', {'form': form})


def review_order(request):
    return render(request, 'orders/order_review.html')
