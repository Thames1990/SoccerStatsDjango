from django.shortcuts import render

from .util import get_or_create_fixtures


def fixtures_view(request, fixture_id):
    return render(request, 'fixture/index.html', {
        'fixtures': get_or_create_fixtures(fixture_id),
    })
