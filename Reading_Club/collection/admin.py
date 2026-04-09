from django.contrib import admin
from Reading_Club.collection.models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'collection_slug', 'created_by']
    search_fields = ['title']

