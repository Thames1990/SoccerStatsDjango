from django.contrib import admin

from .models import LeagueTable, Standing, Home, Away, CupTable, Group, GroupStanding

admin.site.register(LeagueTable)
admin.site.register(Standing)
admin.site.register(Home)
admin.site.register(Away)
admin.site.register(CupTable)
admin.site.register(Group)
admin.site.register(GroupStanding)
