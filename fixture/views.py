from django.views.generic import DetailView, ListView

from .models import Fixture


class FixtureDetailView(DetailView):
    model = Fixture
    context_object_name = 'fixture'


class FixtureListView(ListView):
    model = Fixture
    context_object_name = 'fixtures'
