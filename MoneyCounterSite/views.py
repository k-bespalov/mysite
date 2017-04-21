# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
import json
import dateutil.parser as dt
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

from MoneyCounterSite.forms import RegistrationForm, AddPayment
from MoneyCounterSite.models import *
from .forms import AddParty


# @login_required(login_url="/login/")
def party_list(request):
    parties = Party.objects.filter(persons__user__username=auth.get_user(request).username).order_by('-datetime')[:20]
    return JsonResponse({
        'parties': [
            {
                'id': p.id,
                'name': p.name,
                'datetime': p.datetime,
                'place': p.place,
                'participants': len(Profile.objects.filter(party=p.id)),
                'cost': count_cost_party(p.id),
                'persons': [{'photo': person.photo.url} for person in
                            Profile.objects.filter(party=p)]

            } for p in parties
        ]
    })


def add_party(request):
    tmp = json.loads(request.body)
    tmp['datetime'] = dt.parse(tmp['datetime'])
    form = AddParty(tmp)
    if form.is_valid():
        name = form.cleaned_data['name']
        datetime = form.cleaned_data['datetime']
        place = form.cleaned_data['place']
        p = Party(name=name, datetime=datetime, place=place)
        p.save()
        profile = Profile.objects.get(user__username=auth.get_user(request).username)
        p.persons.add(profile)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


# @require_POST
# @csrf_protect
def add_payment(request):
    form = AddPayment(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        description = form.cleaned_data['description']
        cost = form.cleaned_data['cost']
        p = Payment(description=description, cost=cost)
        p.save()
        profile = Profile.objects.get(user__username=auth.get_user(request).username)
        party = Party.objects.get(id=id)
        p.p_user = profile
        p.p_party = party
        participants = Profile.objects.filter(party__id=id)
        for participant in participants:
            if participant.id != id:
                r = Repayment(price=(cost/len(participants)))
                r.save()
                r.who_pays = participant
                r.who_receives = profile
                r.which_party = party
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def friends_list(request):
    user = auth.get_user(request).username
    friends = Profile.objects.filter(friends__user__username=user).values_list('id', flat=True)[:20]
    return JsonResponse({
        'friends': [
            {
                'id': f,
                'photo': Profile.objects.get(id=f).photo.url,
                'username': User.objects.filter(profile=f).values_list('username', flat=True)[0],
                'name': ' '.join([User.objects.filter(profile=f).values_list('first_name', flat=True)[0],
                        User.objects.filter(profile=f).values_list('last_name', flat=True)[0] ]),
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
            'id': party.id,
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
            'photo': profile.photo.path,
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
    payments = Payment.objects.filter(p_user__user__username=auth.get_user(request).username).order_by('-datetime')[:20]
    return JsonResponse({
        'payments': [
            {
                'datetime': payment.datetime,
                'party': payment.p_party.name,
                'party_id': payment.p_party_id,
                'description': payment.description,
                'cost': payment.cost,
                'persons': [{'photo': person.photo.url} for person in
                            Profile.objects.filter(party=payment.p_party_id)]
            } for payment in payments
        ]
    })


def count_cost_party(party_id):
    payments = Payment.objects.filter(p_party__id=party_id).values_list('cost', flat=True)
    return sum(payments)


# def registration(request):
#     if request.method == 'POST':
#         args = {}
#         args.update(csrf(request))
#         args['form'] = RegistrationForm(request.POST)
#         if args['form'].is_valid():
#             password1 = args['form'].cleaned_data['password1']
#             password2 = args['form'].cleaned_data['password2']
#             if password1 != password2:
#                 args['form'].add_error('password1', "Пароли не совпадают")
#                 return render(request, 'core/registration.html', args)
#             captcha = args['form'].cleaned_data['captcha']
#             if captcha != 22:
#                 args['form'].add_error('captcha', "Каптча не совпадает")
#                 return render(request, 'core/registration.html', args)
#             username = args['form'].cleaned_data['username']
#             first_name = args['form'].cleaned_data['first_name']
#             last_name = args['form'].cleaned_data['last_name']
#             email = args['form'].cleaned_data['email']
#             telephone_number = args['form'].cleaned_data['telephone_number']
#             photo = args['form'].cleaned_data['photo']
#             try:
#                 u = User(
#                     username=username,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                 )
#                 u.set_password(password1)
#                 u.save()
#             except IntegrityError:
#                 args['form'].add_error(
#                     'username',
#                     "The username is already in use"
#                 )
#                 return render(request, 'core/registration.html', args)
#             p = Profile(user_id=u.id, telephone_number=telephone_number, photo=photo)
#             p.save()
#             return redirect('/auth/login/')
#     else:
#         args = {}
#         args.update(csrf(request))
#         args['form'] = RegistrationForm()
#     return render(request, 'core/registration.html', args)

def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)
    return d


# @csrf_exempt
# def my_view(request):
#     if request.POST:
#         print(request.body)
#         req_body = json.loads(request.body)
#         # req_body = binary_to_dict(request.body)
#         print(req_body)
#         username = req_body['username']
#         # print(username)
#         password = req_body['password']
#         # print(password)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print('ok')
#             return HttpResponseRedirect('/parties')
#             # return redirect('/parties')
#         else:
#             print('no ok')
#             return render(request, 'core/login.html')
#     else:
#         return HttpResponse(status=200)
# @csrf_protect
def my_login(request):
    # print(request.method == 'POST')
    if request.method == 'GET':
        return HttpResponse(status=200)
    if request.method == 'POST':
        # print('ok')
        # username = request.POST.get('username', '')
        # print(username)
        # password = request.POST.get('password', '')
        req_body = json.loads(request.body)
        # req_body = binary_to_dict(request.body)
        # print(req_body)
        username = req_body['username']
        # print(username)
        password = req_body['password']
        # print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print('ok')
            return HttpResponse(status=200)
        else:
            # args['login_error'] = "Тусовщие не найден"
            return HttpResponse(status=304)
    else:
        return HttpResponse(status=403)
#
#
# def logout(request):
#     auth.logout(request)
#     return redirect('/')
