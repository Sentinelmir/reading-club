from django.contrib import admin
from Reading_Club.author.models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['publishing_name', 'real_name', 'author_slug']
    search_fields = ['publishing_name', 'real_name']

