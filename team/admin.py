from django.contrib import admin

from .models import Team


class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'id',
                'competition',
                'name',
                'code',
                'short_name',
                'squad_market_value',
                'crest_url',
            ]
        }),
    ]
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
