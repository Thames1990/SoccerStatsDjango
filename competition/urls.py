from django.conf.urls import url

from .views import CompetitionsDetailView, CompetitionListView

app_name = 'competition'
urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        CompetitionsDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^$',
        CompetitionListView.as_view(),
        name='list'
    ),
]
