from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from Reading_Club.book.models import Book
from Reading_Club.review.forms import ReviewForm
from Reading_Club.review.models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        book = get_object_or_404(Book, book_slug=self.kwargs['slug'])
        form.instance.book = book
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'slug': self.object.book.book_slug})

class ReviewEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'slug': self.object.book.book_slug})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('books:details', kwargs={'slug': self.object.book.book_slug})