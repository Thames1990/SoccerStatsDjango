from django.contrib import admin

from .models import Fixture, Result, HalfTime, ExtraTime, PenaltyShooutout, Odds

admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(HalfTime)
admin.site.register(ExtraTime)
admin.site.register(PenaltyShooutout)
admin.site.register(Odds)
