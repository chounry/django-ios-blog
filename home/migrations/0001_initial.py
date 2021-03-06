# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-22 06:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(max_length=5000)),
                ('post_img', models.FileField(blank=True, null=True, upload_to='')),
                ('post_title', models.CharField(db_index=True, max_length=100)),
                ('publish_datetime', models.DateTimeField(auto_now=True)),
                ('publish_date', models.DateField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('tag', models.CharField(max_length=2000)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish_datetime'],
            },
        ),
    ]
