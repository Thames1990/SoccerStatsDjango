from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView

from .models import Player


class PlayerDetailView(DetailView):
    model = Player
    context_object_name = 'player'


class PlayerListView(ListView):
    model = Player
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PlayerListView, self).get_context_data(**kwargs)
        players = Player.objects.all()
        paginator = Paginator(players, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            players = paginator.page(page)
        except PageNotAnInteger:
            players = paginator.page(1)
        except EmptyPage:
            players = paginator.page(paginator.num_pages)

        context['players'] = players
        return context
