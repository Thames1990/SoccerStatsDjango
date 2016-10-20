from django.conf.urls import url

from .views import TeamDetailView, TeamListView

app_name = 'team'
urlpatterns = [
    url(
        r'^(?P<pk>[0-9]+)/$',
        TeamDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^$',
        TeamListView.as_view(),
        name='list'
    ),
]
