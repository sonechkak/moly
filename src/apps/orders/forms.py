from django import forms

from apps.users.models import ShippingAddress


class ShippingForm(forms.ModelForm):
    """Адрес доставки."""

    class Meta:
        model = ShippingAddress
        fields = ('state', 'city', 'street')
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Область/край'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица, дом, квартира'}),
        }
        labels = {
            'state': 'Область/край',
            'city': 'Город',
            'street': 'Улица, дом, квартира',
        }
