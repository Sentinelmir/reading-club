from django.urls import path

from Reading_Club.review.views import ReviewCreateView, ReviewEditView, ReviewDeleteView

app_name = 'reviews'

urlpatterns = [
    path('book/<slug:slug>/add/', ReviewCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', ReviewEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete'),
]