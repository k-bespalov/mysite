from django.contrib import admin
from MoneyCounterSite.models import Profile, Party, Payment, Like, Dislike

admin.site.register(Profile)
admin.site.register(Party)
admin.site.register(Payment)
admin.site.register(Like)
admin.site.register(Dislike)
