from django.urls import path, include

from Reading_Club.collection.views import CollectionListView, CreateCollectionView, CollectionDetailsView, CollectionEditView, CollectionDeleteView

app_name = 'collections'

urlpatterns = [
    path('', CollectionListView.as_view(), name='list'),
    path('add/', CreateCollectionView.as_view(), name='create'),
    path('<slug:slug>/', include(
        [
            path('', CollectionDetailsView.as_view(), name='details'),
            path('edit/', CollectionEditView.as_view(), name='edit'),
            path('delete/', CollectionDeleteView.as_view(), name='delete'),
        ]
    ))
]