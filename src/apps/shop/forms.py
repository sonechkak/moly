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


class CustomerForm(forms.ModelForm):
    """Контактная информация."""

    class Meta:
        # model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }


class ShippingForm(forms.ModelForm):
    """Адрес доставки."""

    class Meta:
        # model = ShippingAddress
        fields = ('state', 'city', 'street')
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Область/край'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица, дом, квартира'}),
        }
