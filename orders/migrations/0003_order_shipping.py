# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-20 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20171118_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.BooleanField(choices=[(True, '\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0432 \u043f\u0440\u0435\u0434\u0435\u043b\u0430\u0445 \u0412\u041e \u041c\u043e\u0441\u043a\u0432\u044b'), (False, '\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437')], default=True, verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438'),
        ),
    ]
