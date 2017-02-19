import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView

from .models import Table
from .utils import get_table_changes, get_tables_current_matchday

logger = logging.getLogger(__name__)


class TableDetailView(DetailView):
    model = Table
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super(TableDetailView, self).get_context_data(**kwargs)
        context['table_changes'] = get_table_changes(self.object)
        return context


class TableListView(ListView):
    model = Table
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TableListView, self).get_context_data(**kwargs)
        tables = list(get_tables_current_matchday())
        paginator = Paginator(tables, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            tables = paginator.page(page)
        except PageNotAnInteger:
            tables = paginator.page(1)
        except EmptyPage:
            tables = paginator.page(paginator.num_pages)

        context['tables'] = tables
        # TODO Add table changes

        return context
