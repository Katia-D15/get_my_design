from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm, CommentForm
from .models import Order
from .utils import automatic_price


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

            order.price = automatic_price(order)
            order.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your order was saved successfully'
                                 )
            return redirect(
                'review_order', order_number=order.order_number
                )
    else:
        form = OrderForm()

    return render(request, 'orders/request_your_design.html', {'form': form})


def review_order(request, order_number):
    '''
    Manage and Review an order
    '''
    order = get_object_or_404(
        Order, order_number=order_number.upper(), user=request.user)
    editing = False
    form = OrderForm(instance=order)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            editing = True

        elif action == 'save_edit':
            form = OrderForm(request.POST, request.FILES, instance=order)
            if form.is_valid():
                updated_order = form.save(commit=False)
                updated_order.price = automatic_price(updated_order)
                updated_order.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Order updated successfully.'
                                     )
                return redirect(
                    'review_order',
                    order_number=order.order_number)
            else:
                editing = True
        elif action == 'cancel':
            order.status = 'cancelled'
            order.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your order has been cancelled.'
                        )
            return redirect('home')

        elif action == 'pay':
            return redirect('home')

    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/order_review.html', {
        'order': order,
        'form': form,
        'editing': editing,
    })


@login_required
def my_orders(request):
    '''
    Display user's orders
    '''
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


def previous_work(request):
    '''
    Render the "Previous Work" page showing all approved comments
    for completed orders. Includes a comment form for the logged-in
    user's completed orders.
    '''
    orders = Order.objects.filter(status='completed').order_by('-created_at')

    for order in orders:
        order.comments_approved = order.comments.filter(
            approved=True).order_by('-created_at')
        if request.user.is_authenticated and order.user == request.user:
            order.comment_form = CommentForm()
        else:
            order.comment_form = None

    context = {
        'orders': orders,
    }
    return render(request, 'orders/previous_work.html', context)


@login_required
def submit_comment(request, order_id):
    '''
    Handle comment submission for a completed order belonging
    to the logged-in user. Saves the comment with approved=False
    and redirects to the "Previous Work" page.
    '''
    order = get_object_or_404(
        Order, pk=order_id,
        user=request.user,
        status='completed'
        )

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.order = order
            comment.approved = False
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval.')

    return redirect('previous_work')
