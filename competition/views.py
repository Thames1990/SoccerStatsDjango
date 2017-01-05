from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView

from .models import Competition


class CompetitionDetailView(DetailView):
    model = Competition
    context_object_name = 'competition'


class CompetitionListView(ListView):
    model = Competition
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CompetitionListView, self).get_context_data(**kwargs)
        competitions = Competition.objects.all()
        paginator = Paginator(competitions, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            competitions = paginator.page(page)
        except PageNotAnInteger:
            competitions = paginator.page(1)
        except EmptyPage:
            competitions = paginator.page(paginator.num_pages)

        context['competitions'] = competitions
        return context
