from django.contrib import admin

from .models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odds

admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(HalfTime)
admin.site.register(ExtraTime)
admin.site.register(PenaltyShootout)
admin.site.register(Odds)
