# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0003_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='name',
            field=models.CharField(max_length=191, verbose_name='Название тусовки'),
        ),
    ]
