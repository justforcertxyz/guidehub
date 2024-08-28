from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterUserForm
from django.views.generic.edit import CreateView
from guide.models import Guide


class IndexView(TemplateView):
    template_name = "landing/index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "landing/privacy_policy.html"


class ImprintView(TemplateView):
    template_name = "landing/imprint.html"


class LoginUserView(LoginView):
    template_name = "landing/login.html"
    next_page = reverse_lazy("landing:index")


class LogoutUserView(LoginRequiredMixin, LogoutView):
    http_method_names = ["get", "post"]
    template_name = "landing/logout.html"
    next_page = reverse_lazy("landing:index")
    login_url = "landing:login"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterUserView(CreateView):
    template_name = "landing/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("landing:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "landing/dashboard.html"
    login_url = "landing:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guides_owned"] = [guide for guide in Guide.objects.all().order_by(
            'current_price')[:3] if guide.is_owned(self.request.user)]
        context["guides_written"] = [guide for guide in Guide.objects.all().order_by(
            'current_price')[:3] if guide.author == self.request.user]
        return context

from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import time
from django.http import HttpResponse
from payment.models import Order

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
        session_id = session.get('id', None)
        print(f"{session=}")
        line_items = stripe.checkout.Session.list_line_items(session_id)
        order = Order.objects.get(stripe_checkout_id=session_id)
        print(f"{order.user=}")

    return HttpResponse(status=200)
