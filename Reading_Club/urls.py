from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Reading_Club.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="homepage"),
    path('accounts/', include('Reading_Club.accounts.urls')),
    path('book/', include('Reading_Club.book.urls')),
    path('collection/', include('Reading_Club.collection.urls')),
    path('review/', include('Reading_Club.review.urls')),
    path('author/', include('Reading_Club.author.urls')),
    path('api/', include('Reading_Club.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)