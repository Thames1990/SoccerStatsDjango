from django.contrib import admin

from .models import Competition


# TODO Modify Admin for each model
class CompetitionAdmin(admin.ModelAdmin):
    search_fields = ('caption', 'year')


admin.site.register(Competition, CompetitionAdmin)
