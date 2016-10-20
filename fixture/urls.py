from django.conf.urls import url

from .views import FixtureDetailView, FixtureListView

app_name = 'fixture'
urlpatterns = [
    url(
        r'^(?P<pk>[0-9]+)/$',
        FixtureDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^$',
        FixtureListView.as_view(),
        name='list'
    ),
]
