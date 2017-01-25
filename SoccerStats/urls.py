from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^competitions/', include('competition.urls')),
    url(r'^fixtures/', include('fixture.urls')),
    url(r'^players/', include('player.urls')),
    url(r'^tables/', include('table.urls')),
    url(r'^teams/', include('team.urls')),
    url(r'^football-data.events/api_token.txt', TemplateView.as_view(
        template_name='SoccerStats/api_token.txt',
        content_type='text/plain',
    )),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

handler403 = views.error403
handler404 = views.error404
handler500 = views.error500
