# Generated by Django 5.1 on 2024-08-24 20:22

import django.core.files.storage
import django.utils.timezone
import pathlib
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Post Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('html_file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=pathlib.PurePosixPath('/home/ok/Documents/Python/guidehub/GuideHub/blog/templates/blog/entries')), upload_to='', verbose_name='HTML File')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
