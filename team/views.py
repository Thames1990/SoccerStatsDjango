from django.views.generic import DetailView, ListView

from .models import Team


class TeamDetailView(DetailView):
    model = Team
    context_object_name = 'team'


class TeamListView(ListView):
    model = Team
    context_object_name = 'teams'
