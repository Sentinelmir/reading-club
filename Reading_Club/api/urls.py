from django.urls import path
from Reading_Club.api.views import AuthorsListAPI, BooksListAPI

app_name = 'api'

urlpatterns = [
    path('authors/', AuthorsListAPI.as_view(), name = 'authors-list-api'),
    path('books/', BooksListAPI.as_view(), name= 'books-list-api')
]