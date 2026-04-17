from rest_framework import serializers

from Reading_Club.author.models import Author
from Reading_Club.book.models import Book


class BookApiSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.publishing_name', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'name',
            'book_slug',
            'genre',
            'author',
            'author_name',
            'pages',
            'description',
            'year_of_publishing',
            'book_cover',
            'created_by',
            'average_rating',
        ]
        read_only_fields = ['book_slug', 'created_by', 'average_rating', 'author_name']


class AuthorApiSerializer(serializers.ModelSerializer):
    books = BookApiSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'publishing_name', 'real_name', 'books']