from django.shortcuts import render
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order


@csrf_exempt
def stripe_webhook_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print(f"ValueError: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"SignatureVerificationError: {e}")
        return HttpResponse(status=400)

    if (event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'):
        session = event['data']['object']
        _fullfill_checkout(session)

    return HttpResponse(status=200)


def _fullfill_checkout(session):
    if session.payment_status != 'unpaid':
        session_id = session.get('id', None)
        line_items = stripe.checkout.Session.list_line_items(session_id)
        order = Order.objects.get(stripe_checkout_id=session_id)
        order.payment_complete = True
        order.price = line_items["data"][0]["amount_total"]/100
        
        order.guide.add_owner(order.user)

        order.save()
        print(f"{order.price}")
