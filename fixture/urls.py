from django.conf.urls import url

from .views import FixtureDetailView, FixtureListView

app_name = 'fixture'
urlpatterns = [
    url(
        r'^$',
        FixtureListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        FixtureDetailView.as_view(),
        name='detail'
    ),
]
