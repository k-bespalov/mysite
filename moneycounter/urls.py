"""moneycounter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
import MoneyCounterSite.urls
from MoneyCounterSite.views import *

urlpatterns = [
    url(r'^parties$', party_list, name='party_list'),
    url(r'^parties/add/$', add_party, name='add_party'),
    url(r'^id(?P<id>\d+)/$', show_profile, name='show_profile'),
    url(r'^friends$', friends_list, name='friends_list'),
    url(r'^payments$', my_payments_list, name='my_payments_list'),
    url(r'^participants(?P<party_id>\d+)/$', show_party_participants, name='show_party_participants'),
    url(r'^party(?P<party_id>\d+)/$', party_detail, name='party_detail'),
    url(r'^', include(MoneyCounterSite.urls, namespace='MoneyCounterSite')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login, {'template_name': 'core/login.html'}),
    url(r'^logout/', logout, {'template_name': 'core/logout.html'}),
]
