# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-16 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0015_auto_20170407_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='photos/None/no-img.jpg', upload_to='photos/'),
        ),
    ]