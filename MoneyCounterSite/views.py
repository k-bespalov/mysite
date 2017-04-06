# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib import auth
from MoneyCounterSite.models import *


def party_list(request):
    parties = Party.objects.filter(persons__user__username=auth.get_user(request).username)[:20]
    return JsonResponse({
        'parties': [
            {
                'id': p.id,
                'name': p.name,
                'datetime': p.datetime,
                'cost': count_cost_party(p.id),
                'participants': len(Profile.objects.filter(party=p.id))
            } for p in parties
        ]
    })


def friends_list(request):
    user = auth.get_user(request).username
    friends = Profile.objects.filter(friends__user__username=user).values_list('id', flat=True)[:20]
    return JsonResponse({
        'friends': [
            {
                'id': f,
                'username': User.objects.filter(profile=f).values_list('username', flat=True)[0],
                'first_name': User.objects.filter(profile=f).values_list('first_name', flat=True)[0],
                'last_name': User.objects.filter(profile=f).values_list('last_name', flat=True)[0],
                # 'photo': f.photo}
            } for f in friends
        ]
    })


def party_detail(request, party_id):
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        raise Http404
    return JsonResponse(
        {
            'name': party.name,
            'datetime': party.datetime,
            'place': party.place,
            'cost': count_cost_party(party_id),
            'likes': like_dislike_counter(2, party_id)[0],
            'dislikes': like_dislike_counter(2, party_id)[1],
            'persons': [{'id': person.id, 'first_name': User.objects.get(id=person.user_id).first_name,
                         'last_name': User.objects.get(id=person.user_id).last_name} for person in
                        Profile.objects.filter(party=party_id)]
        })


def show_party_participants(request, party_id):
    participants = Profile.objects.filter(party__id=party_id).values_list('id', flat=True)[:20]
    return JsonResponse({
        'participants': [
            {
                'id': p,
                'first_name': User.objects.filter(profile=p).values_list('first_name', flat=True)[0],
                'last_name': User.objects.filter(profile=p).values_list('last_name', flat=True)[0],

            } for p in participants
        ]
    })


def show_profile(request, id):
    profile = Profile.objects.get(id=id)
    goods = FavouriteGoods.objects.filter(person=id).values_list('name', flat=True)
    user = profile.user
    return JsonResponse(
        {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'telephone_number': profile.telephone_number,
            'likes': like_dislike_counter(3, id)[0],
            'dislikes': like_dislike_counter(3, id)[1],
            'favourite_goods': [item for item in goods]
        }
    )


def like_dislike_counter(content, object):
    counter = [0, 0]
    list = Like.objects.filter(content_type=content, object_id=object).values_list('positive', flat=True)
    for flag in list:
        if flag:
            counter[0] += 1
        else:
            counter[1] += 1
    return counter


def my_payments_list(request):
    payments = Payment.objects.filter(p_user__user__username=auth.get_user(request).username)[:20]
    return JsonResponse({
        'payments': [
            {
                'datetime': payment.datetime,
                'party': payment.p_party.name,
                'description': payment.description,
                'cost': payment.cost
            } for payment in payments
        ]
    })


def count_cost_party(party_id):
    payments = Payment.objects.filter(p_party__id=party_id).values_list('cost', flat=True)
    return sum(payments)
