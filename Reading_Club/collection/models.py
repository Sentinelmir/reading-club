from django.db import models
from django.utils.text import slugify

from Reading_Club import settings
from Reading_Club.book.models import Book


class Collection(models.Model):
    title = models.CharField(max_length=120, blank=False)
    collection_slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_collection", null=True, blank=True)
    books = models.ManyToManyField(Book, related_name='collections')
    cover = models.ImageField(upload_to="collection_covers/", blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.collection_slug:
            self.collection_slug = slugify(self.title)
        super().save(*args, **kwargs)
