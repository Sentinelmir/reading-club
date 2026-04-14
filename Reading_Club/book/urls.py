from django.urls import path, include
from Reading_Club.book.views import BooksListView, BookDetailsView, AddNewBookView, EditBookView, DeleteBookView, toggle_read, toggle_favorite

app_name = 'books'

urlpatterns = [
    path('', BooksListView.as_view(), name='list'),
    path('add_new_book/', AddNewBookView.as_view(), name='add'),
    path('<slug:slug>/', include(
        [
            path('', BookDetailsView.as_view(), name='details'),
            path('edit/', EditBookView.as_view(), name='edit'),
            path('delete/', DeleteBookView.as_view(), name='delete'),
        ]
    ),
),
    path('<slug:slug>/favorite/', toggle_favorite, name='favorite'),
    path('<slug:slug>/read/', toggle_read, name='read'),
]