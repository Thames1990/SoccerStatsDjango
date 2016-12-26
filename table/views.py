from django.views.generic import DetailView, ListView

from .models import Table

from .utils import get_table_changes


class TableDetailView(DetailView):
    model = Table
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super(TableDetailView, self).get_context_data(**kwargs)
        context['table_changes'] = get_table_changes(self.object)
        return context


class TableListView(ListView):
    model = Table
    context_object_name = 'tables'
