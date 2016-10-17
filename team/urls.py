from django.conf.urls import url

from . import views

app_name = 'team'
urlpatterns = [
    url(
        r'^(?P<team_id>[0-9]+)/$',
        views.team_view,
        name='team'
    ),
]
