# import os, sys
# proj_path = "/home/konstantin/web_sphere/mysite"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moneycountersite.settings")
# sys.path.append(proj_path)
# os.chdir(proj_path)
#



from MoneyCounterSite.models import *
import random
import datetime
import string
from django.utils import timezone

USERS_NUM = 100
NAMES_NUM = 60
SURNAMES_NUM = 251
PARTIES_NUM = 50
PAYMENT_NUM = 10



first_names = []
last_names = []

with open('first_names.txt', 'r') as file:
    for line in file:
        line = line[:-1]
        first_names.extend( line.split('\t') )


with open('last_names.txt', 'r') as file:
    for line in file:
        last_names.append(line[:-1])

favouritegoods  = ["чипсы", "пицца", "сухарики", "салат цезарь", "шаурма",
 "суши", "роллы", "бургеры", "сухарики", "конфеты", "мармелад", "кортошка фри",
  "крылья", "пиво", "шаипанское", "вино", "виски", "ликер", "водка"]


def password_gen():
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(8))
    return password

def username_gen():
    username_size = random.randint(6, 16)
    chars = string.ascii_letters
    username = ''.join(random.choice(chars) for _ in range(username_size))
    return username

def email_gen():
    email_size = random.randint(5, 10)
    chars = string.ascii_lowercase + string.digits
    letter = random.choice(string.ascii_lowercase)
    email = ''.join(random.choice(chars) for _ in range(email_size))
    email = letter + email
    email += '@mail.ru'
    return email

def telephone_number_gen():
    dig = string.digits
    number = ''.join(random.choice(dig) for _ in range(9))
    number = '+79' + number
    return number

def first_name_gen():
    i = random.randint(0, NAMES_NUM-1)
    return first_names[i]

def last_name_gen():
    i = random.randint(0, SURNAMES_NUM-1)
    return last_names[i]

def party_name_gen():
    dig = string.digits
    name_size = random.randint(5, 10)
    name = ''.join(random.choice(dig) for _ in range(name_size))
    name = 'туса номер ' + name
    return name

def place_name_gen():
    dig = string.digits
    name_size = random.randint(5, 10)
    name = ''.join(random.choice(dig) for _ in range(name_size))
    name = 'место номер ' + name
    return name

def description_gen(arr):
    return ''.join(random.sample(arr, random.randint(1, len(arr))))[:-1]




BULK_NUM = 10

for _ in range(BULK_NUM):
    users_list = []
    for _ in range(int(USERS_NUM / BULK_NUM)):
        user_tmp = User(
            username = username_gen(),
            first_name = first_name_gen(),
            last_name = last_name_gen(),
            email = email_gen(),
            password = password_gen()
        )
        users_list.append(user_tmp)
    User.objects.bulk_create(users_list)


user_counter = 0
all_users = list(User.objects.all().values_list('id', flat=True))
for _ in range(BULK_NUM):
    profile_list = []
    for _ in range(int(USERS_NUM / BULK_NUM)):
        profile_tmp = Profile(
            user_id = all_users[user_counter],
            telephone_number = telephone_number_gen()
        )
        user_counter += 1
        profile_list.append(profile_tmp)
    Profile.objects.bulk_create(profile_list)


for _ in range(BULK_NUM):
    party_list = []
    for _ in range(int(PARTIES_NUM / BULK_NUM)):
        # personss = list(User.objects.all().values_list('id', flat=True))
        # person_list = [].extend(random.sample(personss, random.randint(1, USERS_NUM)))
        year = random.choice(range(2015, 2017))
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        hour = random.choice(range(0, 24))
        minute = random.choice(range(0, 60))
        second = random.choice(range(0, 60))
        party_tmp = Party(
            name = party_name_gen(),
            datetime=timezone.datetime(year, month, day, hour, minute, second),
            place = place_name_gen(),
            #persons = person_list,
            total_cost = random.randint(1000, 4000)
        )
        party_list.append(party_tmp)
    Party.objects.bulk_create(party_list)
#
# print('13311441')
#
# all_profiles = list(Profile.objects.all())
# all_parties = list(Party.objects.all())
# for party in all_parties:
#     tmp_profiles_list = []
#     tmp_profiles_list.extend(random.sample(all_profiles, random.randint(1, 25)))
#     party.persons.add(tmp_profiles_list)
#
# print('er3rhio')



for _ in range(BULK_NUM):
    payment_list = []
    for _ in range(int(PAYMENT_NUM / BULK_NUM)):
        year = random.choice(range(2015, 2017))
        month = random.choice(range(1, 13))
        day = random.choice(range(1, 29))
        hour = random.choice(range(0, 24))
        minute = random.choice(range(0, 60))
        second = random.choice(range(0, 60))
        payment_tmp = Party(
            datetime=timezone.datetime(year, month, day, hour, minute, second),
            p_user = Profile.objects.get(id=(random.randint(0, USERS_NUM))),
            p_party = Party.objects.get(id=(random.randint(0, PARTIES_NUM))),
            description = description_gen(favouritegoods),
            cost = random.randint(100, 600)
        )
        payment_list.append(payment_tmp)
    Payment.objects.bulk_create(payment_list)


for _ in range(BULK_NUM):
    repayment_list = []
    for _ in range(int(PAYMENT_NUM / BULK_NUM)):
        repayment_tmp = Party(
            who_pays_id = Profle.objects.get(id=(random.randint(0, USERS_NUM))),
            which_party_id = Party.objects.get(id=(random.randint(0, PARTIES_NUM))),
            who_receives_id = Profle.objects.get(id=(random.randint(0, USERS_NUM))),
            price = random.randint(100, 600)
        )
        repayment_list.append(payment_tmp)
    Repayment.objects.bulk_create(repayment_list)


# for i in range(len(favouritegoods)):
#     goods_list = []
#     personss = list(User.objects.all().values_list('id', flat=True))
#     goods_tmp = FavouriteGoods(
#         name = favouritegoods[i]
#     )
#     goods_list.append(goods_tmp)
# FavouriteGoods.objects.bulk_create(goods_list)
#
#
# all_profiles = list(Profile.objects.all())
# all_goods = list(FavouriteGoods.objects.all())
# for item in all_goods:
#     tmp_profiles_list = []
#     tmp_profiles_list.extend(random.sample(all_profiles, random.randint(1, USERS_NUM)))
#     item.persons.add(tmp_profiles_list)
