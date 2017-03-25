# import os, sys
# proj_path = "/home/konstantin/web_sphere/mysite"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moneycountersite.settings")
# sys.path.append(proj_path)
# os.chdir(proj_path)
#



# from MoneyCounterSite.models import *
import random
import datetime
import string
from django.utils import timezone

USERS_NUM = 100000
NAMES_NUM = 60
SURNAMES_NUM = 251
PARTIES_NUM = 100000



first_names = []
last_names = []

with open('first_names.txt', 'r') as file:
    for line in file:
        line = line[:-1]
        first_names.extend( line.split('\t') )


with open('last_names.txt', 'r') as file:
    for line in file:
        last_names.append(line[:-1])

print(len(last_names))


def password_gen():
    password_size = random.randint(8, 16)
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(password_size))
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
    i = random.randint(0, NAMES_NUM)
    return first_names[i]

def last_name_gen():
    i = random.randint(0, SURNAMES_NUM)
    return last_names[i]
