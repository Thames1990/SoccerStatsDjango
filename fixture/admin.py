from django.contrib import admin

from .models import Fixture, Result, HalfTime, ExtraTime, PenaltyShootout, Odd


class FixtureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'id',
                'competition',
                'status',
            ]
        }),
        ('Zeitangaben', {
            'fields': [
                'date',
                'matchday',
            ]
        }),
        ('Mannschaften', {
            'fields': [
                'home_team',
                'away_team',
            ]
        }),
    ]
    list_display = (
        'id',
        'competition',
        'home_team',
        'away_team',
        'date',
        'status',
        'matchday',
    )
    list_filter = (
        'status',
        'matchday',
    )
    readonly_fields = (
        'id',
    )
    search_fields = [
        'competition__caption',
        'home_team__name',
        'away_team__name',
    ]


class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'fixture',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals_home_team',
                'goals_away_team',
            ]
        }),
    ]
    list_display = (
        'fixture',
        'goals_home_team',
        'goals_away_team',
    )
    list_filter = (
        'fixture__status',
        'fixture__matchday',
    )
    search_fields = [
        'fixture__status',
    ]


class HalfTimeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'result',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals_home_team',
                'goals_away_team',
            ]
        }),
    ]
    list_display = (
        'result',
        'goals_home_team',
        'goals_away_team',
    )
    list_filter = (
        'result__fixture__status',
        'result__fixture__matchday',
    )
    search_fields = [
        'result__fixture__status',
    ]


class ExtraTimeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'result',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals_home_team',
                'goals_away_team',
            ]
        }),
    ]
    list_display = (
        'result',
        'goals_home_team',
        'goals_away_team',
    )
    list_filter = (
        'result__fixture__status',
        'result__fixture__matchday',
    )
    search_fields = [
        'result__fixture__status',
    ]


class PenaltyShootoutAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'result',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals_home_team',
                'goals_away_team',
            ]
        }),
    ]
    list_display = (
        'result',
        'goals_home_team',
        'goals_away_team',
    )
    list_filter = (
        'result__fixture__status',
        'result__fixture__matchday',
    )
    search_fields = [
        'result__fixture__status',
    ]


class OddAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'fixture',
            ]
        }),
        ('Wettchancen', {
            'fields': [
                'home_win',
                'draw',
                'away_win',
            ]
        }),
    ]
    list_display = (
        'fixture',
        'home_win',
        'draw',
        'away_win',
    )
    list_filter = (
        'fixture__status',
        'fixture__matchday',
    )
    search_fields = [
        'fixture__status',
    ]


admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(HalfTime, HalfTimeAdmin)
admin.site.register(ExtraTime, ExtraTimeAdmin)
admin.site.register(PenaltyShootout, PenaltyShootoutAdmin)
admin.site.register(Odd, OddAdmin)
