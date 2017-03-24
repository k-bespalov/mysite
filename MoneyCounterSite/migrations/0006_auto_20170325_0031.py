# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0005_auto_20170325_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='total_cost',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=5, null=True, verbose_name='Общая стоимость тусы'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Сколько заплатил'),
        ),
    ]