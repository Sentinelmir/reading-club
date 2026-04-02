from django.urls import path, include
from Reading_Club.author.views import AuthorCreateView, AuthorDetailsView, AuthorDeleteView, AuthorEditView

app_name = 'autor'

urlpatterns = [
    path('add_new/', AuthorCreateView.as_view(), name='create'),
    path('<slug:author_slug>', include(
            [
                path('', AuthorDetailsView.as_view(), name='details'),
                path('edit/', AuthorEditView.as_view(), name='edit'),
                path('', AuthorDeleteView.as_view(), name='delete'),
            ]
        ),
    ),
]