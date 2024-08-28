from django.shortcuts import render, get_object_or_404
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from guide.models import Guide
import stripe


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


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "payment/checkout.html"
    login_url = "landing:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guide"] = get_object_or_404(
            Guide, slug=self.request.GET.get('guide'))
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        guide = get_object_or_404(Guide, slug=kwargs['slug'])

        ## if request.user.is_authenticated:
        ##     # TODO: What if inactive -> Shouldnt be shown at all
        ##     if guide.is_active:
        ##         try:
        ##             checkout_session = stripe.checkout.Session.create(line_items=[{"price": guide.stripe_price_id,
        ##                                                                            "quantity": 1}],
        ##                                                               mode='payment',
        ##                                                               invoice_creation={
        ##                                                                   "enabled": True},
        ##                                                               automatic_tax={
        ##                                                                   "enabled": True},
        ##                                                               # success_url=f"{
        ##                                                               #     reverse('guide:payment-success')}",
        ##                                                               # cancel_url=f"{reverse('guide:payment-failed')}")
        ##                                                               success_url="http://127.0.0.1:8000/guide/erfolgreich",
        ##                                                               cancel_url="http://127.0.0.1:8000/guide/abgebrochen")
        ##             order = Order.create_order(
        ##                 guide, guide.current_price, request.user, stripe_checkout_id=checkout_session["id"])

        ##             return redirect(checkout_session.url, code=303)
        ##         except Exception as e:
        ##             print(f"Exception: {e}")
        ##             raise Http404
        ## return HttpResponseRedirect(reverse('landing:login'))