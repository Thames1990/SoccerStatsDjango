from django.contrib import admin

from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'team',
                'name',
                'position',
                'jersey_number',
                'nationality',
                'market_value',
                'image',
            ]
        }),
        ('Zeitangaben', {
            'fields': [
                'date_of_birth',
                'contract_until',
            ]
        }),
    ]
    list_display = (
        'team',
        'name',
        'position',
        'jersey_number',
        'date_of_birth',
        'nationality',
        'contract_until',
        'market_value',
        'image',
    )
    list_filter = (
        'position',
        'nationality',
    )
    search_fields = [
        'team__name',
        'name',
        'position',
        'nationality',
    ]


admin.site.register(Player, PlayerAdmin)
