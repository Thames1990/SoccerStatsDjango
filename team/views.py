from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView

from .models import Team


class TeamDetailView(DetailView):
    model = Team
    context_object_name = 'team'


class TeamListView(ListView):
    model = Team
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        teams = Team.objects.all()
        paginator = Paginator(teams, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            teams = paginator.page(page)
        except PageNotAnInteger:
            teams = paginator.page(1)
        except EmptyPage:
            teams = paginator.page(paginator.num_pages)

        context['teams'] = teams
        return context
