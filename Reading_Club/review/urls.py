from django.urls import path
from Reading_Club.review.views import ReviewListView

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='list'),
]