from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from Reading_Club.api.permissions import IsOwnerOrAdminOrReadOnly
from Reading_Club.api.serializers import AuthorApiSerializer, BookApiSerializer
from Reading_Club.author.models import Author
from Reading_Club.book.models import Book


class AuthorsListAPI(ListAPIView):
    queryset = Author.objects.prefetch_related("books").all()
    serializer_class = AuthorApiSerializer
    permission_classes = [AllowAny]


class BooksListAPI(ListCreateAPIView):
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookApiSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BookDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('author', 'created_by').all()
    serializer_class = BookApiSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]