# -*- coding: utf-8 -*-

from django import forms

from MoneyCounterSite.models import Profile, Party


class AddPayment(forms.Form):
    party = forms.ChoiceField(choices=Party.objects.all())
    description = forms.CharField(label='Описание платежа', max_length=200)
    cost = forms.DecimalField(label='Стоимость', max_digits=9, decimal_places=2)


class AddParty(forms.Form):
    name = forms.CharField(label='Название тусы')
    datetime = forms.DateTimeField(label='Дата тусовки')
    place = forms.CharField(label='Место проведения')
    participants = forms.ModelMultipleChoiceField(queryset=Profile.objects.all())


class EditParty(forms.Form):
    name = forms.CharField(label='Название тусы')
    datetime = forms.DateTimeField(label='Дата тусовки')
    place = forms.CharField(label='Место проведения')


class AddFavouriteGoods(forms.Form):
    name = forms.CharField(label='Предпочтение или несколько')


class EditProfile(forms.Form):
    first_name = forms.CharField(label='Введите имя')
    last_name = forms.CharField(label='Введите фамилию')
    telephone_number = forms.CharField(label='Номер телефона', min_length=12, max_length=12)
    photo = forms.ImageField(label='Фото профиля')


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Введите имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'special'}))
    first_name = forms.CharField(label='Введите имя',
                                 widget=forms.TextInput(attrs={'class': 'special'}))
    last_name = forms.CharField(label='Введите фамилию',
                                widget=forms.TextInput(attrs={'class': 'special'}))
    email = forms.EmailField(max_length=100,
                             widget=forms.TextInput(attrs={'class': 'special'}))
    number = forms.CharField(label='Номер телефона', min_length=12, max_length=12,
                             widget=forms.TextInput(attrs={'class': 'special'}))
    photo = forms.ImageField(label='Фото профиля')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'special'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'special'})
    )
    captcha = forms.IntegerField(label='12 + ten = ',
                                 widget=forms.TextInput(attrs={'class': 'special'}))
