# Generated by Django 5.1 on 2024-08-22 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0002_alter_guide_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='Thumbnal'),
        ),
    ]
