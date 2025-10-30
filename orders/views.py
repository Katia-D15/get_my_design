from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .forms import OrderForm, CommentForm
from .models import Order, Comment
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


@login_required
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

    Anonymous users see only completed orders that already have
    approved comments (no forms).

    Logged-in users see all completed orders, even those without
    comments. for their own completed orders, a comment form is
    available.

    The page also supports editing or deleting an existing
    comment from the logged-in user.
    '''
    orders = Order.objects.filter(status='completed').order_by('-created_at')

    if not request.user.is_authenticated:
        orders = orders.filter(comments__approved=True).distinct()

    for order in orders:
        order.comments_approved = order.comments.filter(
            approved=True).order_by('-created_at')

        can_comment = (
            request.user.is_authenticated
            and order.user_id == request.user.id
            and order.status == 'completed'
        )
        order.comment_form = CommentForm() if can_comment else None

    editing_id = request.GET.get("edit")
    edit_form = None
    if editing_id and request.user.is_authenticated:
        try:
            comment = Comment.objects.get(pk=editing_id, user=request.user)
            edit_form = CommentForm(instance=comment)
            editing_id = int(editing_id)
        except (Comment.DoesNotExist, ValueError):
            editing_id = None
            edit_form = None

    deleting_id = request.GET.get("delete")
    try:
        deleting_id = int(deleting_id) if deleting_id else None
    except (TypeError, ValueError):
        deleting_id = None

    context = {
        'orders': orders,
        'editing_id': editing_id,
        'edit_form': edit_form,
        'deleting_id': deleting_id,
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


@login_required
def edit_comment(request, comment_id):
    '''
    Allow a logged-in user to edit their own comment.
    On Post, saves the edited comment as unapproved (requires re-approval)
    and redirects with a success message.
    '''

    comment = get_object_or_404(
        Comment, pk=comment_id,
        user=request.user
        )

    if request.method != 'POST':
        return redirect(f"{reverse('previous_work')}?edit={comment_id}")

    form = CommentForm(request.POST, request.FILES, instance=comment)
    if form.is_valid():
        comment_edited = form.save(commit=False)
        comment_edited.approved = False
        comment_edited.save()
        messages.add_message(
            request, messages.SUCCESS,
            'Comment updated and sent for re-approval.'
        )
        return redirect('previous_work')


@login_required
def delete_comment(request, comment_id):
    '''
    Allow a logged-in user to delete their own comment.
    '''

    comment = get_object_or_404(
        Comment, pk=comment_id,
        user=request.user,
        order__status='completed',
    )

    if request.method != 'POST':
        return redirect(
            f"{reverse('previous_work')}?delete={comment_id}"
            f"#order-{comment.order_id}")

    order_id = comment.order_id
    comment.delete()
    messages.add_message(
        request, messages.SUCCESS,
        'Comment deleted successfully'
    )
    return redirect(f"{reverse('previous_work')}#order-{order_id}")


only_moderators = user_passes_test(
    lambda u: u.is_active and (u.is_staff or u.is_superuser))


@login_required
@only_moderators
def approve_comment(request, comment_id):
    '''
    Allow staff or superuser to approve comment
    '''
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.approved = True
        comment.save(update_fields=["approved"])
        messages.add_message(
            request, messages.SUCCESS,
            'Comment approved'
            )
    return redirect(request.META.get("HTTP_REFERER", "moderation_queue"))


@login_required
@only_moderators
def reject_comment(request, comment_id):
    '''
    Allow staff or superuser to reject comment
    '''
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.approved = False
        comment.save(update_fields=["approved"])
        messages.add_message(
            request, messages.SUCCESS,
            'Comment rejected'
            )
    return redirect(request.META.get("HTTP_REFERER", "moderation_queue"))


@login_required
@only_moderators
def moderation_queue(request):
    '''
    Display all comments with False value
    '''
    comments = Comment.objects.filter(
        approved=False).select_related("user", "order").order_by("created_at")
    return render(request, 'orders/rate_comments.html', {"comments": comments})
