# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-07 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441:'),
        ),
    ]
