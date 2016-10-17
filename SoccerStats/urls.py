from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^competition/', include('competition.urls')),
    url(r'^fixture/', include('fixture.urls')),
    url(r'^player/', include('player.urls')),
    url(r'^table/', include('table.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

handler403 = views.error403
handler404 = views.error404
handler500 = views.error500
