from django.shortcuts import render, get_object_or_404
from django.conf import settings
import stripe
from orders.models import Order


def checkout(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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
