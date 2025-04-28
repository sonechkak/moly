from django import forms


class CouponForm(forms.Form):
    """Форма для применения купона."""

    coupon = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Введите промокод", "class": "form-control"})
    )
