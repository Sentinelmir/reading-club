from celery import shared_task
from PIL import Image

from Reading_Club.book.models import Book


@shared_task
def resize_book_cover(book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return

    if not book.book_cover:
        return

    image_path = book.book_cover.path

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail((600, 900))
        img.save(image_path, format="JPEG", quality=85)