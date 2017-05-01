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
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from datetime import tzinfo, timedelta, datetime
from django.template.context_processors import csrf
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

from MoneyCounterSite.forms import RegistrationForm, AddPayment, AddParty
from MoneyCounterSite.models import *


# @login_required(login_url="/login/")
def party_list(request):
    parties_list = Party.objects.filter(persons__user__username=auth.get_user(request).username).order_by('-datetime')
    paginator = Paginator(parties_list, 1)
    page = json.loads(request.body)['page']
        # request.GET.get('page')
    # print(page)
    try:
        parties = paginator.page(page)
        # print(parties)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        parties = paginator.page(1)
        # print(parties)
    except EmptyPage:
        return HttpResponse(status=200)
        # If page is out of range (e.g. 9999), deliver last page of results.
        # parties = paginator.page(paginator.num_pages)
        # print(parties)
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
                            Profile.objects.filter(party=p)],

            } for p in parties
        ],
        'next_page': paginator.page(page).has_next(),
    })


def party_change(request, party_id):
    print(request.method == 'GET')
    party = Party.objects.get(id=int(party_id))
    if request.method == 'GET':
        # participants = party.persons.values_list('id', flat=True)
        return JsonResponse({
            'name': party.name,
            'participants': [],
            'place': party.place,
            'date': party.datetime.date(),
            'time': party.datetime.time()
        })
    if request.method == 'POST':
        for person in Profile.objects.filter(party__id=int(party_id)):
            party.persons.remove(person)
        tmp = json.loads(request.body)
        tmp['datetime'] = dt.parse(tmp['datetime'])
        form = AddParty(tmp)
        if form.is_valid():
            party.name = form.cleaned_data['name']
            party.datetime = form.cleaned_data['datetime']
            party.place = form.cleaned_data['place']
            # p = Party(name=name, datetime=datetime, place=place)
            party.save()
            participants_id = tmp['participants']
            profile = Profile.objects.get(user__username=auth.get_user(request).username)
            party.persons.add(profile)
            if participants_id != []:
                for id in participants_id:
                    party.persons.add(Profile.objects.get(id=id))
                return HttpResponse(status=200)
            else:
                friends = Profile.objects.filter(friends__id=profile.id)
                for friend in friends:
                    party.persons.add(friend)
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    return HttpResponse(status=403)



def add_party(request):
    if request.method == 'GET':
        friends = Profile.objects.filter(friends__user__id=request.user.id)
        response_data = {
            'friends': [{
                'id': friend.id,
                'name': ' '.join([User.objects.filter(profile=friend.id).values_list('first_name', flat=True)[0],
                                  User.objects.filter(profile=friend.id).values_list('last_name', flat=True)[0]]),
            } for friend in friends]
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if request.method == 'POST':
        tmp = json.loads(request.body)
        tmp['datetime'] = dt.parse(tmp['datetime'])
        form = AddParty(tmp)
        if form.is_valid():
            name = form.cleaned_data['name']
            datetime = form.cleaned_data['datetime']
            place = form.cleaned_data['place']
            p = Party(name=name, datetime=datetime, place=place)
            p.save()
            participants_id = tmp['participants']
            profile = Profile.objects.get(user__username=auth.get_user(request).username)
            p.persons.add(profile)
            if participants_id != []:
                for id in participants_id:
                    p.persons.add(Profile.objects.get(id=id))
                return HttpResponse(status=200)
            else:
                friends = Profile.objects.filter(friends__id=profile.id)
                for friend in friends:
                    p.persons.add(friend)
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)


# @require_POST
# @csrf_protect
def add_payment(request):
    if request.method == 'GET':
        # print('ok')
        date = datetime.today()
        # print(date.month)
        parties = Party.objects.filter(persons__user__username=auth.get_user(request).username,
                                       datetime__year=date.year).order_by('-datetime')
        return JsonResponse({
            'parties': [
                {
                    'id': party.id,
                    'name': party.name
                } for party in parties
            ]
        })
    if request.method == 'POST':
        tmp = json.loads(request.body)
        form = AddPayment(tmp)
        print(form.errors)
        if form.is_valid():
            id = form.cleaned_data['id']
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']
            payers = [int(x) for x in tmp['payers']]
            print(payers)
            profile = Profile.objects.get(user__username=auth.get_user(request).username)
            party = Party.objects.get(id=id)
            p = Payment(p_user=profile, p_party=party, description=description, cost=cost)
            p.save()
            if payers != []:
                participants = []
                for payer in payers:
                    if Profile.objects.get(user__id=request.user.id).id != payer:
                        participants.append(Profile.objects.get(id=payer))
                for participant in participants:
                        r = Repayment(who_pays=participant, who_receives=profile, which_party=party,
                                      price=(cost / len(payers)))
                        r.save()
                return HttpResponse(status=200)
            else:
                participants = Profile.objects.filter(~Q(user__username='konstantin')).filter(party__id=id)
                for participant in participants:
                        r = Repayment(who_pays=participant, who_receives=profile, which_party=party,
                                      price=(cost / (len(participants) + 1)))
                        r.save()
                return HttpResponse(status=201)
        else:
            return HttpResponse(status=403)


def get_payers(request):
    id = json.loads(request.body)
    payers = Profile.objects.filter(party__id=id)
    response_data = {
        'payers': [{
            'id': payer.id,
            'name': ' '.join([User.objects.filter(profile=payer.id).values_list('first_name', flat=True)[0],
                              User.objects.filter(profile=payer.id).values_list('last_name', flat=True)[0]]),
        } for payer in payers]
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


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
                                  User.objects.filter(profile=f).values_list('last_name', flat=True)[0]]),
            } for f in friends
        ]
    })


def to_me_repayments_list(request):
    to_me = Repayment.objects.filter(who_receives__user__id=request.user.id, is_payed=False).order_by('-id')
    return JsonResponse({
        'to_me': [
            {
                'id': rep.id,
                'who_pays':
                    {
                        'photo': rep.who_pays.photo.url,
                        'name': ' '.join([rep.who_pays.user.first_name, rep.who_pays.user.last_name])
                     },
                'which_party':
                    {
                        'party_id': rep.which_party_id,
                        'party_name': rep.which_party.name
                    },
                'price': rep.price,
                'is_payed': rep.is_payed

            } for rep in to_me
        ]
    })


def from_me_repayments_list(request):
    from_me = Repayment.objects.filter(who_pays__user__id=request.user.id, is_payed=False).order_by('-id')
    return JsonResponse({
        'from_me': [
            {
                'who_pays':
                    {
                        'photo': rep.who_receives.photo.url,
                        'name': ' '.join([rep.who_receives.user.first_name, rep.who_receives.user.last_name])
                     },
                'which_party':
                    {
                        'party_id': rep.which_party_id,
                        'party_name': rep.which_party.name
                    },
                'price': rep.price,
                'is_payed': rep.is_payed

            } for rep in from_me
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
            # 'likes': like_dislike_counter(2, party_id)[0],
            # 'dislikes': like_dislike_counter(2, party_id)[1],
            'persons': [{'id': person.id, 'photo': person.photo.url, 'first_name': User.objects.get(id=person.user_id).first_name,
                         'last_name': User.objects.get(id=person.user_id).last_name} for person in
                        Profile.objects.filter(party=party_id)],
            'payments': [
                {'who': ' '.join([User.objects.filter(profile__payment=payment).values_list('first_name', flat=True)[0],
                                  User.objects.filter(profile__payment=payment).values_list('last_name', flat=True)[0]]),
                 'photo': Profile.objects.get(payment=payment).photo.url,
                 'datetime': payment.datetime,
                 'description': payment.description,
                 'cost': payment.cost
                 } for payment in Payment.objects.filter(p_party=party.id).order_by('-datetime')],
        })


def change_friend_status(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        profile = Profile.objects.get(user__id=auth.get_user(request).id)
        try:
            friend = profile.friends.get(id=id)
            profile.friends.remove(friend)
            # return JsonResponse({
            #     'status': False
            # })
        except Profile.DoesNotExist:
            friend = Profile.objects.get(id=id)
            profile.friends.add(friend)

            # return JsonResponse({
            #     'friend_status': True
            # })
        return HttpResponse(status=200)
    else:
        return Http404


def set_payed(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        # print(id)
        repayment = Repayment.objects.get(id=id)
        repayment.is_payed = True
        repayment.save()
        return HttpResponse(status=200)
    else:
        return Http404


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
    # print(id)
    # print(Profile.objects.get(user__id=request.user.id).id)
    # print(int(id) == Profile.objects.get(user__id=request.user.id).id)
    profile = Profile.objects.get(id=int(id))
    goods = FavouriteGoods.objects.filter(person=int(id)).values_list('name', flat=True)
    if int(id) == Profile.objects.get(user=auth.get_user(request)).id:
        # profile = Profile.objects.get(user__id=auth.get_user(request).id)

        return JsonResponse(
            {
                'name': ' '.join([User.objects.filter(profile=int(id)).values_list('first_name', flat=True)[0],
                                  User.objects.filter(profile=int(id)).values_list('last_name', flat=True)[0]]),
                'photo': profile.photo.url,
                'favourite_goods': [item for item in goods]
            }
        )
    else:
        return JsonResponse(
            {
                'id': profile.id,
                'name': profile.user.get_full_name(),
                'photo': profile.photo.url,
                'favourite_goods': [item for item in goods],
                'friend_status': Profile.objects.get(id=Profile.objects.get(user__id=request.user.id).id).friends.filter(id=int(id)).exists()
            }
        )
    # return HttpResponse(status=201)


    # profile = Profile.objects.get(id=id)
    # goods = FavouriteGoods.objects.filter(person=id).values_list('name', flat=True)
    # user = profile.user
    # return JsonResponse(
    #     {
    #         'username': user.username,
    #         'first_name': user.first_name,
    #         'last_name': user.last_name,
    #         'telephone_number': profile.telephone_number,
    #         # 'likes': like_dislike_counter(3, id)[0],
    #         'photo': profile.photo.path,
    #         # 'dislikes': like_dislike_counter(3, id)[1],
    #         'favourite_goods': [item for item in goods]
    #     }
    # )


def show_my_profile_id(request):
    id = Profile.objects.get(user__id=auth.get_user(request).id).id
    return JsonResponse({
        'id': id
    })
    # profile = Profile.objects.get(user__id=auth.get_user(request).id)
    # goods = FavouriteGoods.objects.filter(person=profile.id).values_list('name', flat=True)
    # return JsonResponse(
    #     {
    #         'name': ' '.join([User.objects.filter(profile=profile.id).values_list('first_name', flat=True)[0],
    #                           User.objects.filter(profile=profile.id).values_list('last_name', flat=True)[0]]),
    #         'photo': profile.photo.url,
    #         'favourite_goods': [item for item in goods]
    #     }
    # )


def like_dislike_counter(content, object):
    counter = [0, 0]
    list = Like.objects.filter(content_type=content, object_id=object).values_list('positive', flat=True)
    for flag in list:
        if flag:
            counter[0] += 1
        else:
            counter[1] += 1
    return counter


def find_friends(request):
    text = json.loads(request.body)['text']
    qs = Profile.objects.all()
    for term in text.split():
        qs = qs.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term))
    return JsonResponse({
        'results': [
            {
                'id': profile.id,
                'photo': profile.photo.url,
                'name': profile.user.get_full_name()
            } for profile in qs
        ]
    })


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
