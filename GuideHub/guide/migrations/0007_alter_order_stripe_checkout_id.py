# Generated by Django 5.1 on 2024-08-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0006_order_payment_complete_order_stripe_checkout_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='stripe_checkout_id',
            field=models.CharField(max_length=50, verbose_name='Stripe Checkout ID'),
        ),
    ]
