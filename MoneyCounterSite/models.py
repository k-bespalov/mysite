from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField("self", verbose_name = 'Друзья', db_index = True, blank = True)
    telephone_number = models.CharField(max_length = 12, verbose_name = 'Номер телефона', blank=True)
    # favourite_food = models.CharField(max_length = 200, verbose_name = 'Предпочтения в еде', db_index = True, blank=True)
    # favourite_drinkables = models.CharField(max_length = 200, verbose_name = 'Предпочтения в напитках', db_index = True, blank=True)
    #likes = GenericRelation('MoneyCounterSite.Like', related_query_name='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Тусовщик'
        verbose_name_plural = 'Тусовщики'







class FavouriteGoods(models.Model):
    name = models.CharField(max_length=200, verbose_name = 'Предпочтение', db_index = True)
    person = models.ManyToManyField(Profile, verbose_name = 'Чье предпочтение', db_index = True, blank = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предпочтение'
        verbose_name_plural = 'Предпочтения'







class Party(models.Model):
    name = models.CharField(max_length = 200, verbose_name = 'Название тусовки')
    datetime = models.DateTimeField(verbose_name = 'Дата проведения', db_index = True, blank = True, null = True)
    place = models.CharField(max_length=200, verbose_name = 'Место проведения')
    persons = models.ManyToManyField(to=Profile, verbose_name = 'Участники')
    total_cost = models.FloatField(verbose_name = 'Общая стоимость тусы', db_index = True, blank = True, null = True)
    #likes = GenericRelation('MoneyCounterSite.Like', related_query_name='parties',  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тусовка'
        verbose_name_plural = 'Тусовки'





class Payment(models.Model):
    datetime = models.DateTimeField(verbose_name = 'Дата платежа', blank = True, null = True, default=timezone.now)
    user = models.ForeignKey(to=Profile, verbose_name = 'Чей платеж')
    party = models.ForeignKey(to=Party, verbose_name = 'Для какой тусовки')
    description = models.CharField(max_length=200, verbose_name = 'Описание платежа')
    cost = models.FloatField(verbose_name = 'Сколько заплатил')


    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'





class Repayment(models.Model):
    who_pays = models.ForeignKey(to=Profile, related_name = 'who', verbose_name = 'Кого должен отдать денег')
    who_receives = models.ForeignKey(to=Profile, related_name = 'to_whom', verbose_name = 'Кому должен отдать денег')
    which_party = models.ForeignKey(to=Party, verbose_name = 'За какую тусовку')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = 'Сколько должен отдать денег')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'






class Like(models.Model):
    flag = models.NullBooleanField()
    person = models.ForeignKey(to=Profile, verbose_name  = 'Кто поставил')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Лайк/Дизлайк'
        verbose_name_plural = 'Лайки/Дизлайки'

    def __str__(self):
        return self.flag
