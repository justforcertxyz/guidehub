from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic.list import ListView
from .models import Guide
from django.views.generic.detail import DetailView
from django.http import FileResponse, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import time

User = get_user_model()


class IndexListView(ListView):
    model = Guide
    template_name = "guide/index.html"


class GuideDetailView(DetailView):
    model = Guide
    template_name = "guide/detail.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        guide = get_object_or_404(Guide, slug=kwargs['slug'])

        # TODO: What if inactive -> Shouldnt be shown at all
        if guide.is_active:
            try:
                # TODO: Redirect URLS
                checkout_session = stripe.checkout.Session.create(line_items=[{"price": guide.stripe_price_id,
                                                                               "quantity": 1}],
                                                                  mode='payment',
                                                                  invoice_creation={
                                                                      "enabled": True},
                                                                  automatic_tax={
                                                                      "enabled": True},
                                                                  # success_url=f"{
                                                                  #     reverse('guide:payment-success')}",
                                                                  # cancel_url=f"{reverse('guide:payment-failed')}")
                                                                  success_url="http://127.0.0.1:8000/guide/erfolgreich",
                                                                  cancel_url= "http://127.0.0.1:8000/guide/abgebrochen")
                return redirect(checkout_session.url, code=303)
            except Exception as e:
                print(f"Exception: {e}")
                raise Http404


def download_view(request, *args, **kwargs):
    guide = get_object_or_404(Guide, slug=kwargs['slug'])

    if guide.is_owned(request.user):
        return FileResponse(guide.guide_pdf.open(), as_attachment=True)
    else:
        # TODO: Create not owned page
        return HttpResponseRedirect(reverse('landing:index'))


class PaymentSuccessView(TemplateView):
    template_name = "guide/payment_success.html"


class PaymentFailedView(TemplateView):
    template_name = "guide/payment_failed.html"


# @csrf_exempt
# def stripe_webhook_view(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
# 
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         print(f"ValueError: {e}")
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         print(f"SignatureVerificationError: {e}")
#         return HttpResponse(status=400)
# 
#     if (event['type'] == 'checkout.session.completed'
#             or event['type'] == 'checkout.session.async_payment_succeeded'):
#         session = event['data']['object']
#         session_id = session.get('id', None)
#         print(f"{session=}")
#         line_items = stripe.checkout.Session.list_line_items(session_id)
#         print(f"{line_items=}")
# 
#     return HttpResponse(status=200)
