# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuestEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0413\u043e\u0441\u0442\u0435\u0432\u043e\u0439 email')),
                ('active', models.BooleanField(default=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u0413\u043e\u0441\u0442\u0435\u0432\u043e\u0439 email',
                'verbose_name_plural': '\u0413\u043e\u0441\u0442\u0435\u0432\u044b\u0435 emails',
            },
        ),
    ]
