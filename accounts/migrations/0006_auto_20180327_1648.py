# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-27 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_woked_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='woked_products',
            field=models.BooleanField(default=False, verbose_name='\u041c\u043e\u0436\u0435\u0442 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0442\u044c/\u043f\u0440\u0430\u0432\u0438\u0442\u044c/\u0443\u0434\u0430\u043b\u044f\u0442\u044c \u0442\u043e\u0432\u0430\u0440:'),
        ),
    ]
