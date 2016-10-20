from django.conf.urls import url

from .views import CupTableDetailView, CupTableListView, LeagueTableDetailView, LeagueTableListView

app_name = 'player'
urlpatterns = [
    url(
        r'^cup/(?P<pk>\d+)/$',
        CupTableDetailView.as_view(),
        name='cup_detail'
    ),
    url(
        r'^cup/$',
        CupTableListView.as_view(),
        name='cup_list'
    ),
    url(
        r'^league/(?P<pk>\d+)/$',
        LeagueTableDetailView.as_view(),
        name='league_detail'
    ),
    url(
        r'^league/$',
        LeagueTableListView.as_view(),
        name='league_list'
    ),
]
