from django import forms
from Reading_Club.collection.models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'books', 'cover']

        labels = {'title':'Collection name', 'description':'Description', 'books':'Books list', 'cover':'Collection cover'}

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'books': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'cover':
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.setdefault('class', 'form-select')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            elif not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')