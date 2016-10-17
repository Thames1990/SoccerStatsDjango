from django.conf.urls import url

from . import views
from team.views import teams_view

app_name = 'competition'
urlpatterns = [
    url(
        r'^$',
        views.competitions_view,
        name='competitions'
    ),
    url(
        r'^(?P<competition_id>[0-9]+)/$',
        views.competition_view,
        name='competition'
    ),
    url(
        r'^(?P<competition_id>[0-9]+)/teams$',
        teams_view,
        name='competition'
    ),
]
