from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from Reading_Club.author.forms import AuthorCreateForm, AuthorEditForm
from Reading_Club.author.models import Author

class AuthorsListView(ListView):
    model = Author
    template_name = 'authors/authors_list.html'
    context_object_name = 'authors'

class AuthorDetailsView(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'
    context_object_name = 'author'
    slug_field = 'author_slug'
    slug_url_kwarg = 'author_slug'


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorCreateForm
    template_name = 'authors/author_form.html'

    def get_success_url(self):
        return reverse_lazy('author:details', kwargs={'author_slug': self.object.author_slug})


class AuthorEditView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'authors/author_form.html'
    slug_field = 'author_slug'
    slug_url_kwarg = 'author_slug'

    def get_success_url(self):
        return reverse_lazy('author:details', kwargs={'author_slug': self.object.author_slug})

class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'authors/author_confirm_delete.html'
    success_url = reverse_lazy('author:list')
    slug_field = 'author_slug'
    slug_url_kwarg = 'author_slug'
