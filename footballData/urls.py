from django.conf.urls import url

from . import views

app_name = 'footballData'
urlpatterns = [
    url(
        r'^$',
        views.index_view,
        name='index'
    ),
]
