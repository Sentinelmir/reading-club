from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseUser(AbstractUser):
    nickname = models.CharField(max_length=30, blank=False, unique=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    wishlist = models.ManyToManyField("book.Book", related_name="users_wishlist", blank=True)
    read_list = models.ManyToManyField("book.Book", related_name="users_books_list", blank=True)