from django.urls import path, include

app_name = 'collections'

urlpatterns = [
    path('', CollectionListView.as_view(), name='list'),
    path('add/', CreateCollectionView.as_view(), name='create'),
    path('<slug:collection_slug>', include(
        [
            path('', CollectionDetailsView.as_view(), name='details'),
            path('edit/', CollectionEditView.as_view(), name='edit'),
            path('delete', CollectionDelteView.as_view(), name='delete'),
        ]
    ))
]