from django.conf.urls import url

from .views import PlayerDetailView, PlayerListView

app_name = 'player'
urlpatterns = [

    url(
        r'^$',
        PlayerListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        PlayerDetailView.as_view(),
        name='detail'
    ),
]
