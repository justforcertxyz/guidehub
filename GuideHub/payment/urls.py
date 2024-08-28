
from django.urls import path
from . import views

app_name = "payment"


urlpatterns = [
    path("webhook/", views.stripe_webhook_view, name="stripe-webhook"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]