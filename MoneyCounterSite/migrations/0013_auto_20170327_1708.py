# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 14:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyCounterSite', '0012_auto_20170327_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='party',
            new_name='p_party',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='user',
            new_name='p_user',
        ),
    ]
