# Generated by Django 5.1 on 2024-08-25 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Guide is active'),
        ),
        migrations.AddField(
            model_name='guide',
            name='stripe_url',
            field=models.URLField(blank=True, verbose_name='Stripe Product URL'),
        ),
    ]
