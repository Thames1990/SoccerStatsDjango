from django.contrib import admin

from .models import Table, Standing, HomeStanding, AwayStanding, Group, GroupStanding


class TableAdmin(admin.ModelAdmin):
    list_display = (
        'competition',
        'matchday',
    )
    list_filter = (
        'competition__is_cup',
        'competition__year',
        'matchday',
    )
    search_fields = [
        'competition__caption',
    ]


class StandingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'table',
                'team',
                'position',
                'points',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals',
                'goals_against',
                'goal_difference',
            ]
        }),
        ('Spiele', {
            'fields': [
                'played_games',
                'wins',
                'draws',
                'losses',
            ]
        }),
    ]
    list_display = (
        'table',
        'team',
        'position',
        'played_games',
        'points',
        'goals',
        'goals_against',
        'goal_difference',
        'wins',
        'draws',
        'losses',
    )
    list_filter = (
        'table__competition__is_cup',
        'table__competition__year',
    )
    search_fields = [
        'table__competition__caption',
        'team__name',
    ]


class HomeStandingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'standing',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals',
                'goals_against',
            ]
        }),
        ('Spiele', {
            'fields': [
                'wins',
                'draws',
                'losses',
            ]
        }),
    ]
    list_display = (
        'standing',
        'goals',
        'goals_against',
        'wins',
        'draws',
        'losses',
    )
    list_filter = (
        'standing__table__competition__is_cup',
        'standing__table__competition__year',
    )
    search_fields = [
        'standing__table__competition__caption',
    ]


class AwayStandingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'standing',
            ]
        }),
        ('Tore', {
            'fields': [
                'goals',
                'goals_against',
            ]
        }),
        ('Spiele', {
            'fields': [
                'wins',
                'draws',
                'losses',
            ]
        }),
    ]
    list_display = (
        'standing',
        'goals',
        'goals_against',
        'wins',
        'draws',
        'losses',
    )
    list_filter = (
        'standing__table__competition__is_cup',
        'standing__table__competition__year',
    )
    search_fields = [
        'standing__table__competition__caption',
    ]


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'table',
        'name',
    )
    list_filter = (
        'table__competition__is_cup',
        'table__competition__year',
    )
    search_fields = [
        'table__competition__caption',
        'name',
    ]


class GroupStandingAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'team',
        'rank',
        'played_games',
        'crest_uri',
        'points',
        'goals',
        'goals_against',
    )
    list_filter = (
        'group__table__competition__is_cup',
        'group__table__competition__year',
    )
    search_fields = [
        'group__table__competition__caption',
        'team__name',
    ]


admin.site.register(Table, TableAdmin)
admin.site.register(Standing, StandingAdmin)
admin.site.register(HomeStanding, HomeStandingAdmin)
admin.site.register(AwayStanding, AwayStandingAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupStanding, GroupStandingAdmin)
