from django.views.generic import TemplateView
from Reading_Club.book.models import Book
from Reading_Club.collection.models import Collection


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_books'] = Book.objects.select_related('author').order_by('-id')[:4]
        context['latest_collections'] = Collection.objects.select_related('created_by').prefetch_related('books').order_by('-id')[:4]
        return context