from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView

from .models import Fixture


class FixtureDetailView(DetailView):
    model = Fixture
    context_object_name = 'fixture'


class FixtureListView(ListView):
    model = Fixture
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(FixtureListView, self).get_context_data(**kwargs)
        fixtures = Fixture.objects.all()
        paginator = Paginator(fixtures, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            fixtures = paginator.page(page)
        except PageNotAnInteger:
            fixtures = paginator.page(1)
        except EmptyPage:
            fixtures = paginator.page(paginator.num_pages)

        context['fixtures'] = fixtures
        return context
