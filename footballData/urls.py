from django.conf.urls import url

from . import views

app_name = 'footballData'
urlpatterns = [
    url(
        r'^(?P<competition_id>[0-9]+)/$',
        views.table_view,
        name='table'
    ),
]
