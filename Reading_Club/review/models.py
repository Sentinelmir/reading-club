from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from Reading_Club import settings
from Reading_Club.book.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_author", null=True, blank=True)
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self) -> str:
        return f"{self.book.name} — {self.author.nickname} ({self.rating}/5)"