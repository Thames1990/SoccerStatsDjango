from django.conf.urls import url

from .views import TableDetailView, TableListView

app_name = 'table'
urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        TableDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^$',
        TableListView.as_view(),
        name='list'
    ),
]
