from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Reading_Club.book.forms import BookForm, EditBookForm
from Reading_Club.book.models import Book

class BooksListView(ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books'


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
        return super().form_valid(form)

class EditBookView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = EditBookForm
    template_name = 'books/edit_book.html'
    slug_field = 'book_slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'slug': self.object.book_slug})

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
def toggle_favorite(request, slug):
    book = get_object_or_404(Book, book_slug=slug)

    if book in request.user.wishlist.all():
        request.user.wishlist.remove(book)
    else:
        request.user.wishlist.add(book)

    return redirect('books:list')

@login_required
def toggle_read(request, slug):
    book = get_object_or_404(Book, book_slug=slug)

    if book in request.user.read_list.all():
        request.user.read_list.remove(book)
    else:
        request.user.read_list.add(book)

    return redirect('books:list')