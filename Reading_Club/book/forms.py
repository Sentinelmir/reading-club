from django import forms

from Reading_Club.author.models import Author
from Reading_Club.book.models import Book


class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=50, label='Who wrote the book', help_text='Enter the publishing name of the author.',
        error_messages={'required': 'Please enter an author name.', 'max_length': 'Author name cannot be longer than 50 characters.',},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Agatha Christie'}),
    )

    genre = forms.ChoiceField(
        choices=Book.BookGenre.choices,
        label='Genres',
        error_messages={"required": "You need to choose a genre!"}
    )

    class Meta:
        model = Book
        fields = ['name', 'pages', 'description', 'genre', 'author_name', 'year_of_publishing', 'book_cover']
        labels = {
            'name': 'Book name',
            'pages': 'Pages in the book',
            'description': 'Book description',
            'genre': 'Genre',
            'year_of_publishing': 'Publishing year',
            'book_cover': 'Book cover',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of pages'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Short description'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'year_of_publishing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2005'}),
            'book_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.author:
            self.fields['author_name'].initial = self.instance.author.publishing_name

        for field_name, field in self.fields.items():
            if field_name == 'book_cover':
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            elif not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_author_name(self):
        author_name = self.cleaned_data['author_name'].strip()

        if not author_name:
            raise forms.ValidationError('Please enter an author name.')

        return author_name

    def save(self, commit=True):
        book = super().save(commit=False)
        author_name = self.cleaned_data['author_name']

        author = Author.objects.filter(publishing_name__iexact=author_name).first()
        if not author:
            author = Author.objects.create(publishing_name=author_name)

        book.author = author

        if commit:
            book.save()
            self.save_m2m()

        return book

class EditBookForm(BookForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_name'].disabled = True