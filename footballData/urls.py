from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /leagueTable/
    url(r'^$', views.index, name='index'),
    # ex: /leagueTable/5/
    url(r'^(?P<football_data_id>[0-9]+)/$', views.detail, name='detail')
]