# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 10:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Дизлайки',
                'verbose_name': 'Дизлайк',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Лайки',
                'verbose_name': 'Лайк',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название тусовки')),
                ('datetime', models.DateTimeField(blank=True, null=True, verbose_name='Дата проведения')),
                ('place', models.CharField(max_length=200, verbose_name='Место проведения')),
                ('total_cost', models.FloatField(blank=True, null=True, verbose_name='Общая стоимость тусы')),
            ],
            options={
                'verbose_name_plural': 'Тусовки',
                'verbose_name': 'Тусовка',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True, verbose_name='Дата платежа')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Описание платежа')),
                ('cost', models.FloatField(verbose_name='Сколько заплатил')),
                ('party_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoneyCounterSite.Party', verbose_name='Для какой тусовки')),
            ],
            options={
                'verbose_name_plural': 'Платежи',
                'verbose_name': 'Платеж',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone_number', models.CharField(blank=True, max_length=12, verbose_name='Номер телефона')),
                ('favourite_food', models.CharField(blank=True, max_length=200, verbose_name='Предпочтения в еде')),
                ('favourite_drinkables', models.CharField(blank=True, max_length=200, verbose_name='Предпочтения в напитках')),
                ('friends', models.ManyToManyField(blank=True, db_index=True, related_name='_profile_friends_+', to='MoneyCounterSite.Profile', verbose_name='Друзья')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Тусовщики',
                'verbose_name': 'Тусовщик',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoneyCounterSite.Profile', verbose_name='Чей платеж'),
        ),
        migrations.AddField(
            model_name='party',
            name='persons',
            field=models.ManyToManyField(to='MoneyCounterSite.Profile', verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='like',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoneyCounterSite.Profile', verbose_name='Кто поставил'),
        ),
        migrations.AddField(
            model_name='dislike',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoneyCounterSite.Profile', verbose_name='Кто поставил'),
        ),
    ]
