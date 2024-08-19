# Generated by Django 5.1 on 2024-08-19 20:40

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Guide Text')),
                ('pages', models.PositiveIntegerField(default=1, verbose_name='Amount of Pages')),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Current Guide Price')),
                ('price_history', models.JSONField(blank=True, null=True, verbose_name='Price History')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='Thumbnal')),
                ('guide_pdf', models.FileField(upload_to='doc/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Full Guide PDF')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('owned_by', models.ManyToManyField(blank=True, related_name='owned_by', to=settings.AUTH_USER_MODEL, verbose_name='Owned By')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
