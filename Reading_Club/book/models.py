from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from Reading_Club import settings
from Reading_Club.author.models import Author
from Reading_Club.book.validators import validate_file_size


class Book(models.Model):
    class BookGenre(models.TextChoices):
        FANTASY = "fantasy", "Fantasy"
        DRAMA = "drama", "Drama"
        SCIENCE = "science", "Science"
        ROMANCE = "romance", "Romance"
        MYSTERY = "mystery", "Mystery"
        YOUNG_ADULT = "young adult", "Young adult"

    name = models.CharField(max_length=50, unique=True, blank=False)
    book_slug = models.SlugField(max_length=140, unique=True, blank=True)
    pages = models.PositiveIntegerField(validators=[MinValueValidator(10),], blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)
    genre = models.CharField(choices=BookGenre.choices, default=BookGenre.ROMANCE, max_length=30)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='books', blank=False, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_books", null=True, blank=True)
    year_of_publishing = models.PositiveIntegerField(blank=True, null=True)
    book_cover = models.ImageField(upload_to="books_covers/", blank=True, null=True, validators=[validate_file_size])

    def save(self, *args, **kwargs):
        if not self.book_slug:
            self.book_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        return round(avg, 1) if avg is not None else None


