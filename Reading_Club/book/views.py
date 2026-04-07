from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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
    slug_url_kwarg = 'book_slug'


class AddNewBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EditBookView(UpdateView):
    model = Book
    form_class = EditBookForm
    template_name = 'books/edit_book.html'

    slug_field = 'book_slug'
    slug_url_kwarg = 'book_slug'

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'book_slug': self.object.book_slug})


class DeleteBookView(View):
    pass