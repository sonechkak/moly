from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма для отзыва."""

    class Meta:
        model = Review
        fields = ('text', 'grade',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв'}),
            'grade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ваша оценка'}),
        }
