from django import forms

DELIVERY_METHODS = (
    ("courier", "Курьерская доставка"),
    ("pickup", "Самовывоз из магазина"),
)

PAYMENT_METHODS = (
    ("card_online", "Оплата картой онлайн (Stripe)"),
    ("card_later", "Банковской картой при получении"),
    ("cash", "Наличными при получении"),
)


class OrderForm(forms.Form):
    """Форма для оформления заказа."""

    # Информация о получателе
    recipient = forms.CharField(
        label="Получатель",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "required": "required"}),
    )

    contact = forms.CharField(
        label="Контактный телефон",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 (___) ___-__-__", "required": "required"}
        ),
    )

    city = forms.CharField(
        label="Город", widget=forms.TextInput(attrs={"class": "form-control", "required": "required"})
    )

    state = forms.CharField(
        label="Область/регион", widget=forms.TextInput(attrs={"class": "form-control", "required": "required"})
    )

    street = forms.CharField(
        label="Улица", widget=forms.TextInput(attrs={"class": "form-control", "required": "required"})
    )

    house = forms.CharField(
        label="Дом", widget=forms.TextInput(attrs={"class": "form-control", "required": "required"})
    )

    apartment = forms.CharField(
        label="Квартира", required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    zipcode = forms.CharField(
        label="Почтовый индекс", required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    is_save_address = forms.BooleanField(
        label="Сохранить этот адрес для будущих заказов",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    delivery_method = forms.ChoiceField(
        label="Способ доставки",
        choices=DELIVERY_METHODS,
        initial="courier",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )

    payment_method = forms.ChoiceField(
        label="Способ оплаты",
        choices=PAYMENT_METHODS,
        initial="card_online",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )

    comment = forms.CharField(
        label="Комментарий к заказу",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 2, "placeholder": "Укажите особые пожелания по доставке"}
        ),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, "profile"):
            self.fields["recipient"].initial = str(user.profile)
