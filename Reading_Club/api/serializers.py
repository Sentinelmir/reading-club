from rest_framework import serializers

from Reading_Club.author.models import Author
from Reading_Club.book.models import Book


class BookApiSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.publishing_name", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "name", "genre", "author", "pages"]


class AuthorApiSerializer(serializers.ModelSerializer):
    books = BookApiSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "publishing_name", 'real_name', "books"]