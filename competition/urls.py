from django.conf.urls import url

from .views import CompetitionDetailView, CompetitionListView

app_name = 'competition'
urlpatterns = [
    url(
        r'^$',
        CompetitionListView.as_view(),
        name='list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        CompetitionDetailView.as_view(),
        name='detail'
    ),
]
