# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0006_auto_20170325_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='media/None/no-img.jpg', upload_to='media/'),
        ),
    ]
