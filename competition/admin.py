from django.contrib import admin

from .models import Competition


class CompetitionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'id',
                'is_cup',
                'caption',
                'league',
            ]
        }),
        ('Zeitangaben', {
            'fields': [
                'year',
                'last_updated',
            ]
        }),
        ('Anzahl', {
            'fields': [
                'current_matchday',
                'number_of_matchdays',
                'number_of_teams',
                'number_of_games',
            ]
        }),
    ]
    list_display = (
        'id',
        'is_cup',
        'caption',
        'league',
        'year',
        'current_matchday',
        'number_of_matchdays',
        'number_of_teams',
        'number_of_games',
        'last_updated',
    )
    list_filter = (
        'is_cup',
        'year',
    )
    readonly_fields = (
        'id',
        'is_cup',
        'last_updated',
    )
    search_fields = ['caption']


admin.site.register(Competition, CompetitionAdmin)
