from django.conf.urls import url

from . import views

app_name = 'player'
urlpatterns = [
    url(
        r'^(?P<team_id>[0-9]+)/(?P<player_name>[\w-]+)/$',
        views.index_view,
        name='index'
    ),
]
