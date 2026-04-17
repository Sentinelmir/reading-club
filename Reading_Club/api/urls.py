from django.urls import path
from Reading_Club.api.views import AuthorsListAPI, BooksListAPI, BookDetailAPI

app_name = 'api'

urlpatterns = [
    path('authors/', AuthorsListAPI.as_view(), name = 'authors-list-api'),
    path('books/', BooksListAPI.as_view(), name= 'books-list-api'),
    path('books/<int:pk>/', BookDetailAPI.as_view(), name='book-detail-api'),
]