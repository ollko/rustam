# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-21 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_product_in_stack'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(db_index=True, default=True, verbose_name='\u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'),
        ),
    ]
