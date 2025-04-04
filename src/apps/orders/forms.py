from apps.users.models import ShippingAddress
from django import forms


class ShippingForm(forms.ModelForm):
    """Адрес доставки."""

    class Meta:
        model = ShippingAddress
        fields = ("state", "city", "street", "house", "apartment", "recipient", "contact", "is_save_address")
        widgets = {
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "Область/край"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Город"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Улица, дом, квартира"}),
            "house": forms.TextInput(attrs={"class": "form-control", "placeholder": "Дом"}),
            "apartment": forms.TextInput(attrs={"class": "form-control", "placeholder": "Квартира"}),
            "recipient": forms.TextInput(attrs={"class": "form-control", "placeholder": "Получатель"}),
            "contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Контактный телефон"}),
            "is_save_address": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "state": "Область/край",
            "city": "Город",
            "street": "Улица, дом, квартира",
            "house": "Дом",
            "apartment": "Квартира",
            "recipient": "Получатель",
            "contact": "Контактный телефон",
            "is_save_address": "Сохранить адрес",
        }
