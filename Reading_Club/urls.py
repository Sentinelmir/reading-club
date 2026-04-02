from django.contrib import admin
from django.urls import path, include
from Reading_Club.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="homepage"),
    path('accounts/', include('accounts.urls')),
    path('book/', include('book.urls')),
    path('collection/', include('collection.urls')),
    path('review/', include('review.urls')),
    path('author/', include('author.urls')),

]
