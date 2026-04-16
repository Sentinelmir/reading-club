from django.urls import path

from Reading_Club.review.views import ReviewCreateView, ReviewEditView, ReviewDeleteView, ReviewListView

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='list'),
    path('book/<slug:slug>/add/', ReviewCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', ReviewEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete'),
]