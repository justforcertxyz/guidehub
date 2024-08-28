from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from guide.models import Guide

User = get_user_model()


class Order(models.Model):
    price = models.DecimalField(
        "Price of Order", max_digits=6, decimal_places=2)
    date = models.DateTimeField("Date of Order", default=timezone.now)
    user = models.ForeignKey(
        User, verbose_name="User who ordered", on_delete=models.CASCADE)
    guide = models.ForeignKey(
        Guide, verbose_name="Guide ordered", on_delete=models.CASCADE)
    stripe_checkout_id = models.CharField("Stripe Checkout ID", max_length=50)
    payment_complete = models.BooleanField("Paymant Complete", default=False)

    @classmethod
    def create_order(cls, guide, price, user, stripe_checkout_id):
        return Order.objects.create(guide=guide, price=price, user=user, stripe_checkout_id=stripe_checkout_id)
