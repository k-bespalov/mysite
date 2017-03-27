from django.shortcuts import render
from django.http import Http404
from MoneyCounterSite.models import Party, Profile

def parties_list(request):
    parties = Party.objects.all()[:20]
    return render(
        request, 'parties/party_list.html',
        {'parties': parties}
    )

def party_detail(request, party_id):
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        raise Http404
    return render(
        request, 'parties/party_detail.html',
        {'party' : party}
    )
