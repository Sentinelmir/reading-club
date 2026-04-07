from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from Reading_Club import settings
from Reading_Club.book.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_author", null=True, blank=True)
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])
    date_of_publication = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        author_name = self.author.nickname if self.author else "Anonymous"
        return f"{self.book.name} — {author_name} ({self.rating}/5)"