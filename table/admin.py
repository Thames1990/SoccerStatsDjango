from django.contrib import admin

from .models import Table, Standing, HomeStanding, AwayStanding, Group, GroupStanding

admin.site.register(Table)
admin.site.register(Standing)
admin.site.register(HomeStanding)
admin.site.register(AwayStanding)
admin.site.register(Group)
admin.site.register(GroupStanding)
