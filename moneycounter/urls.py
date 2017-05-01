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
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import moneycounter.settings
from django.conf import settings
from django.contrib.auth.views import logout
import MoneyCounterSite.urls
from MoneyCounterSite.views import party_list, add_party, my_login, show_party_participants, show_profile, friends_list, \
    my_payments_list, party_detail, add_payment, get_payers, show_my_profile_id, change_friend_status, to_me_repayments_list, \
    from_me_repayments_list, set_payed, find_friends, party_change

urlpatterns = [
    url(r'^parties$', party_list, name='party_list'),
    url(r'^party/add$', add_party, name='add_party'),
    url(r'^change_friend_status$', change_friend_status, name='change_friend_status'),
    url(r'^payment/add$', add_payment, name='add_payment'),
    url(r'^id/(?P<id>\d+)$', show_profile, name='show_profile'),
    url(r'^friends$', friends_list, name='friends_list'),
    url(r'^friends/find$', find_friends, name='find_friends'),
    url(r'^profile_id$', show_my_profile_id, name='show_my_profile'),
    url(r'^get/payers$', get_payers, name='get_payers'),
    url(r'^payments$', my_payments_list, name='my_payments_list'),
    url(r'^to_me_repayments$', to_me_repayments_list, name='repayments_list'),
    url(r'^from_me_repayments$', from_me_repayments_list, name='repayments_list'),
    url(r'^set_payed$', set_payed, name='set_payed'),
    url(r'^participants(?P<party_id>\d+)/$', show_party_participants, name='show_party_participants'),
    url(r'^party(?P<party_id>\d+)$', party_detail, name='party_detail'),
    url(r'^party_change(?P<party_id>\d+)$', party_change, name='party_change'),
    url(r'^', include(MoneyCounterSite.urls, namespace='MoneyCounterSite')),
    url(r'^admin/', admin.site.urls),
    url(r'^login', my_login),  # {'template_name': 'core/login.html'}),
    url(r'^logout/', logout, {'template_name': 'core/logout.html'}),
]

if settings.DEBUG:

    if settings.MEDIA_ROOT:
        urlpatterns += static('/media/',

                              document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
