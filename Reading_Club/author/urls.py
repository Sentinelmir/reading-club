from django.urls import path, include
from Reading_Club.author.views import AuthorDetailsView, AuthorDeleteView, AuthorEditView

app_name = 'author'

urlpatterns = [
    path('<slug:author_slug>', include(
            [
                path('', AuthorDetailsView.as_view(), name='details'),
                path('edit/', AuthorEditView.as_view(), name='edit'),
                path('delete/', AuthorDeleteView.as_view(), name='delete'),
            ]
        ),
    ),
]