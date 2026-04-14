from django import forms
from Reading_Club.author.models import Author


class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['publishing_name', 'real_name', 'description', 'photo']
        labels = {
            'publishing_name': 'Publishing name',
            'real_name': 'Real name',
            'description': 'Description',
            'photo': 'Author photo',
        }
        widgets = {
            'publishing_name': forms.TextInput(attrs={'class': 'form-control'}),
            'real_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a short description about the author',
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }