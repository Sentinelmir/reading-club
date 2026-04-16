from io import BytesIO
from celery import shared_task
from django.core.files.base import ContentFile
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

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        original_name = book.book_cover.name.rsplit(".", 1)[0]
        new_file_name = f"{original_name}.jpg"

        book.book_cover.save(new_file_name, ContentFile(buffer.read()), save=False)

    book.save(update_fields=["book_cover"])