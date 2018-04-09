# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-01 11:23
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20180329_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default=None, help_text='\u0411\u0443\u0434\u0435\u0442 \u043b\u0443\u0447\u0448\u0435 \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0444\u043e\u0442\u043e \u0432 \u0444\u043e\u0440\u043c\u0435 \u043a\u0432\u0430\u0434\u0440\u0430\u0442\u0430', null=True, upload_to='pic_of_product/', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
    ]