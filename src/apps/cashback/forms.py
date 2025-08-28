from django import forms


class CashbackApplyForm(forms.Form):
    """Форма для применения кэшбека."""

    use_cashback = forms.BooleanField(
        required=False, label="Применить бонусы", widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    cashback_amount = forms.IntegerField(
        label="Примененные бонусы",
    )
