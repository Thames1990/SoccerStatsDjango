from django.contrib import admin

from .models import Team
from competition.models import Competition


class CompetitionInline(admin.StackedInline):
    model = Competition


class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'id',
                'name',
                'code',
                'short_name',
                'squad_market_value',
                'crest_url',
            ]
        }),
    ]
    inlines = [CompetitionInline]
    list_display = (
        'id',
        'competition',
        'name',
        'code',
        'short_name',
        'squad_market_value',
        'crest_url',
    )
    readonly_fields = (
        'id',
        'crest_url',
    )
    search_fields = [
        'name',
        'short_name',
    ]


admin.site.register(Team, TeamAdmin)
