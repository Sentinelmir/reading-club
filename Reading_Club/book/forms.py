from django import forms
from Reading_Club.book.models import Book


class BookForm(forms.ModelForm):
    genre = forms.ChoiceField(
        choices=Book.BookGenre.choices,
        label='Genres',
        error_messages={"required": "You need to choose a genre!"}
    )

    class Meta:
        model = Book
        fields = ['name', 'pages', 'description', 'genre', 'author', 'year_of_publishing', 'book_cover']

        labels ={'name':'Book name', 'pages': 'Pages in the book', 'description':'Book description', 'genre':'Genre',
                 'author': 'Who wrote the book', 'year_of_publishing':'Publishing year',
                 'book_cover': 'Book cover'}

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'year_of_publishing': forms.NumberInput(attrs={'class': 'form-control'}),
            'book_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'book_cover':
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            elif not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')

class EditBookForm(BookForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True
