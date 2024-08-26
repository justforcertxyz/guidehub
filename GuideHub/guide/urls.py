from django.urls import path
from . import views

app_name = "guide"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("erfolgreich/", views.PaymentSuccessView.as_view(), name="payment-success"),
    path("abgebrochen/", views.PaymentFailedView.as_view(), name="payment-failed"),
    # path("webhook/", views.stripe_webhook_view, name="stripe-webhook"),
    path("<slug:slug>/download", views.download_view, name="download"),
    path("<slug:slug>", views.GuideDetailView.as_view(), name="detail"),
]
