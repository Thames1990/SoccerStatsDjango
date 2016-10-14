from django.conf.urls import url

from . import views

app_name = 'player'
urlpatterns = [
    url(
        r'^(?P<team_id>[0-9]+)/$',
        views.players_view,
        name='players'
    ),
    url(
        r'^(?P<team_id>[0-9]+)/(?P<player_name>[\w-]+)/$',
        views.player_view,
        name='player'
    ),
]
