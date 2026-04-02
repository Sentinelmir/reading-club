from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    publishing_name = models.CharField(max_length=50, blank=False)
    real_name = models.CharField(max_length=50, blank=True)
    author_slug = models.SlugField(max_length=50, blank=True, unique=True)
    photo = models.ImageField(upload_to="authors/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.author_slug:
            self.author_slug = slugify(self.publishing_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.publishing_name
