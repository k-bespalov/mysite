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
import MoneyCounterSite.urls
from MoneyCounterSite.views import parties_list, party_detail

urlpatterns = [
    url(r'^party/list/$', parties_list, name='party_list'),
    url(r'^party_detail/(?P<party_id>\d+)/$', party_detail, name='party_detail'),
    url(r'^', include(MoneyCounterSite.urls, namespace='MoneyCounterSite')),
    url(r'^admin/', admin.site.urls),
]
