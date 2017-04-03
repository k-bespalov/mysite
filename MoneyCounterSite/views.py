from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.contrib import auth
from MoneyCounterSite.models import Party, Profile, User

def party_list(request):
    user = auth.get_user(request).username
    parties = Party.objects.filter(persons__user__username=user)[:20]
    return JsonResponse({
       'parties': [
           {'id': p.id, 'name': p.name, 'date': p.datetime} for p in parties
       ]
    })


def friends_list(request):
    user = auth.get_user(request).username
    friends = Profile.objects.filter(friends__user__username=user)[:20]
    return JsonResponse({
        'friends': [
            {'id': f.id, 'first_name': User.objects.get(id=f.user_id).first_name,
             'last_name': User.objects.get(id=f.user_id).last_name}
             ##'photo': f.photo}##
               for f in friends
        ]
    })


def party_detail(request, party_id):
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        raise Http404
    return JsonResponse(
            {'name': party.name, 'datetime': party.datetime, 'place': party.place,
             'persons': [ {'id': person.id, 'first_name': User.objects.get(id=person.user_id).first_name,
                            'last_name': User.objects.get(id=person.user_id).last_name} for person in Profile.objects.filter(party=party_id)]
    })
