from django.contrib import admin

from .models import Team


class CompetitionInline(admin.TabularInline):
    model = Team.competition.through


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
