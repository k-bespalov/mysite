# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 21:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0003_auto_20170325_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='datetime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата платежа'),
        ),
    ]