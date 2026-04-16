from rest_framework.generics import ListAPIView
from Reading_Club.api.serializers import AuthorApiSerializer, BookApiSerializer
from Reading_Club.author.models import Author
from Reading_Club.book.models import Book


class AuthorsListAPI(ListAPIView):
    queryset = Author.objects.prefetch_related("books").all()
    serializer_class = AuthorApiSerializer

class BooksListAPI(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookApiSerializer