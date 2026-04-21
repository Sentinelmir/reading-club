from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Reading_Club.book.forms import BookForm, EditBookForm
from Reading_Club.book.models import Book
from Reading_Club.book.tasks import resize_book_cover
from django.views.decorators.http import require_POST

class BooksListView(ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.select_related('author')

        genre = self.request.GET.get('genre')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')

        if genre:
            queryset = queryset.filter(genre=genre)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if sort == 'title_asc':
            queryset = queryset.order_by('name')
        elif sort == 'title_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'year_asc':
            queryset = queryset.order_by('year_of_publishing', 'name')
        elif sort == 'year_desc':
            queryset = queryset.order_by('-year_of_publishing', 'name')
        else:
            queryset = queryset.order_by('-id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Book.BookGenre.choices
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['search_value'] = self.request.GET.get('search', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        if self.request.user.is_authenticated:
            context['user_wishlist_ids'] = set(
                self.request.user.wishlist.values_list('id', flat=True)
            )
        else:
            context['user_wishlist_ids'] = set()
        return context


class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    slug_field = 'book_slug'
    slug_url_kwarg = 'slug'


class AddNewBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if self.object.book_cover:
            resize_book_cover.delay(self.object.pk)
        return response

class EditBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = EditBookForm
    template_name = 'books/edit_book.html'
    slug_field = 'book_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'slug': self.object.book_slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get("book_cover"):
            resize_book_cover.delay(self.object.pk)
        return response

class DeleteBookView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy('books:list')
    slug_field = 'book_slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.created_by or self.request.user.is_superuser

@login_required
@require_POST
def toggle_favorite(request, slug):
    book = get_object_or_404(Book, book_slug=slug)

    if book in request.user.wishlist.all():
        request.user.wishlist.remove(book)
    else:
        request.user.wishlist.add(book)

    return redirect(request.META.get('HTTP_REFERER', reverse('books:list')))

@login_required
@require_POST
def toggle_read(request, slug):
    book = get_object_or_404(Book, book_slug=slug)

    if book in request.user.read_list.all():
        request.user.read_list.remove(book)
    else:
        request.user.read_list.add(book)

    return redirect(request.META.get('HTTP_REFERER', reverse('books:list')))