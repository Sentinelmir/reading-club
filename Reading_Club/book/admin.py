from django.contrib import admin
from Reading_Club.book.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_slug', 'genre', 'author', 'created_by']
    search_fields = ['name', 'book_slug', 'genre', 'author__publishing_name']
