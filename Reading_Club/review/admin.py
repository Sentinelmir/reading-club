from django.contrib import admin
from Reading_Club.review.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'text', 'author', 'rating', 'date_of_publication']
    search_fields = ['author', 'rating', 'date_of_publication', 'book__name']
