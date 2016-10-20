from django.views.generic import DetailView, ListView

from .models import Player


class PlayerDetailView(DetailView):
    model = Player
    context_object_name = 'player'


class PlayerListView(ListView):
    model = Player
    context_object_name = 'players'
