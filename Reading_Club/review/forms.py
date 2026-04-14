from django import forms

from Reading_Club.review.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        coerce=int,
        label='Rating',
    )

    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {'text': 'Review text', 'rating': 'Rating'}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your review here',
            }),
        }