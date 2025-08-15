from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe
from orders.models import Order


@require_POST
def cache_checkout_data(request):
    """
    Store additional metadata on Stripe PaymentIntent
    before payment confirmation
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user.email
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry your payment cannot be \
            processed right now. Please  try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request, order_number):
    """
    Handle the checkout process for an existing order
    """
    order = get_object_or_404(Order, order_number=order_number)

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        try:
            if order.status == 'pending':
                order.status = 'confirmed'
                order.save()
            return redirect(
                'checkout_success', order_number=order.order_number)
        except Exception as e:
            return render(request, 'checkout/error.html', {'error': str(e)})

    stripe_total = round(order.price * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        'order': order,
        'stripe_public_key': stripe_public_key,
        'stripe_secret_key': stripe_secret_key,
        'client_secret': intent.client_secret,
              }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Render the checkout success page and attempt
    to email a confirmation to the authenticated user.
    """
    order = get_object_or_404(Order, order_number=order_number)

    recipient = request.user.email

    sent = 0

    try:
        sent = send_mail(
            subject=f"Payment confirmed - Order #{order.order_number}",
            message=render_to_string("checkout/emails/payment_success.txt",
                                     {"order": order}),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False
        )
    except Exception:
        pass

    if sent:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Order successfully Confirmed!'
            f'A confirmation email has been sent sent to {recipient}')
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "We couldn't send the confirmation email right now.")

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
