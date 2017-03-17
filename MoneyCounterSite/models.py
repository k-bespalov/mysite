from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Profile(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField("self", verbose_name = 'Друзья', db_index = True, blank = True)
    telephone_number = models.CharField(max_length = 12, verbose_name = 'Номер телефона', blank=True)
    favourite_food = models.CharField(max_length = 200, verbose_name = 'Предпочтения в еде', blank=True)
    favourite_drinkables = models.CharField(max_length = 200, verbose_name = 'Предпочтения в напитках', blank=True)
    likes = GenericRelation('MoneyCounterSite.Like', related_query_name='profiles', blank=True, null=True)
    dislikes = GenericRelation('MoneyCounterSite.Like', related_query_name='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Тусовщик'
        verbose_name_plural = 'Тусовщики'


class Party(models.Model):
    name = models.CharField(max_length = 200, verbose_name = 'Название тусовки')
    datetime = models.DateTimeField(verbose_name = 'Дата проведения', blank = True, null = True)
    place = models.CharField(max_length=200, verbose_name = 'Место проведения')
    persons = models.ManyToManyField(to=Profile, verbose_name = 'Участники')
    total_cost = models.FloatField(verbose_name = 'Общая стоимость тусы', blank = True, null = True)
    likes = GenericRelation('MoneyCounterSite.Like', related_query_name='parties',  blank=True, null=True)
    dislikes = GenericRelation('MoneyCounterSite.Like', related_query_name='parties',  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тусовка'
        verbose_name_plural = 'Тусовки'

class Payment(models.Model):
    datetime = models.DateTimeField(verbose_name = 'Дата платежа', blank = True, null = True)
    user_id = models.ForeignKey(to=Profile, verbose_name = 'Чей платеж')
    party_id = models.ForeignKey(to=Party, verbose_name = 'Для какой тусовки')
    description = models.CharField(max_length=200, verbose_name = 'Описание платежа', blank = True)
    cost = models.FloatField(verbose_name = 'Сколько заплатил')



    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Like(models.Model):
    person = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name  = 'Кто поставил')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Dislike(models.Model):
    person = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name  = 'Кто поставил')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Дизлайк'
        verbose_name_plural = 'Дизлайки'
