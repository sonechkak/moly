from django import forms

from .models import Profile, ShippingAddress


class ShippingForm(forms.ModelForm):
    """Адрес доставки."""

    class Meta:
        model = ShippingAddress
        fields = [
            "title",
            "state",
            "city",
            "street",
            "house",
            "apartment",
            "zipcode",
            "recipient",
            "contact",
            "is_save_address",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название адреса"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "Область/край"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Город"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Улица, дом, квартира"}),
            "house": forms.TextInput(attrs={"class": "form-control", "placeholder": "Дом"}),
            "apartment": forms.TextInput(attrs={"class": "form-control", "placeholder": "Квартира"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Индекс почты"}),
            "recipient": forms.TextInput(attrs={"class": "form-control", "placeholder": "Получатель"}),
            "contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Контактный телефон"}),
            "is_save_address": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Название адреса",
            "state": "Область/край",
            "city": "Город",
            "street": "Улица, дом, квартира",
            "house": "Дом",
            "apartment": "Квартира",
            "zipcode": "Индекс почты",
            "recipient": "Получатель",
            "contact": "Контактный телефон",
            "is_save_address": "Сохранить адрес",
        }
