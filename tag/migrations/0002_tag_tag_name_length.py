# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-13 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_name_length',
            field=models.PositiveIntegerField(null=True),
        ),
    ]