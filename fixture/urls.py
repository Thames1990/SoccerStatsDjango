from django.conf.urls import url

from . import views

app_name = 'fixture'
urlpatterns = [
    url(
        r'^(?P<fixture_id>[0-9]+)/$',
        views.fixtures_view,
        name='index'
    ),
]
