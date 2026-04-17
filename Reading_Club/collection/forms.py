from django import forms
from Reading_Club.collection.models import Collection

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'books', 'cover']
        labels = {
            'title': 'Collection name',
            'description': 'Description',
            'books': 'Books in this collection',
            'cover': 'Collection cover',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'books': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }