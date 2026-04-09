from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from Reading_Club.collection.forms import CollectionForm
from Reading_Club.collection.models import Collection


class CollectionListView(ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'

class CreateCollectionView(CreateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    success_url = reverse_lazy('collections:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CollectionDetailsView(DetailView):
    model = Collection
    template_name = 'collections/collection_details.html'
    context_object_name = 'collection'

    slug_field = 'collection_slug'

class CollectionEditView(UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = 'collections/collection_form.html'
    slug_field = 'collection_slug'

    def get_success_url(self):
        return reverse_lazy('collections:details', kwargs={'slug': self.object.collection_slug})

class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'collections/delete_collection.html'
    success_url = reverse_lazy('collections:list')
    slug_field = 'collection_slug'
