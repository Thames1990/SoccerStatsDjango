from django.contrib import admin

from .models import LeagueTable, Standing, Home, Away

admin.site.register(LeagueTable)
admin.site.register(Standing)
admin.site.register(Home)
admin.site.register(Away)
