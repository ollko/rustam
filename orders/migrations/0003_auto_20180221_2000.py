# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-21 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20180212_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.Product', verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0437\u0430\u043a\u0430\u0437\u0430'),
        ),
    ]
