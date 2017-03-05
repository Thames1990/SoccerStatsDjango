from django.conf.urls import url

from .views import TeamDetailView, TeamListView

app_name = 'team'
urlpatterns = [
    url(
        r'^$',
        TeamListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        TeamDetailView.as_view(),
        name='detail'
    ),
]
