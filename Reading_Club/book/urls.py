from django.urls import path, include
from Reading_Club.book.views import BooksListView, BookDetailsView, AddNewBookView, EditBookView, DeleteBookView

app_name = 'books'

urlpatterns = [
    path('', BooksListView.as_view(), name='list'),
    path('add_new_book/', AddNewBookView.as_view(), name='add'),
    path('<slug:book_slug>/', include(
        [
            path('', BookDetailsView.as_view(), name='details'),
            path('edit/', EditBookView.as_view(), name='edit'),
            path('delete/', DeleteBookView.as_view(), name='delete'),
        ]
    ),
),
]