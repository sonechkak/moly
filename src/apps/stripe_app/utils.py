import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def handle_stripe_payment(self, order):
    """Перенаправляет на оплату в Stripe."""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "rub",
                        "product_data": {
                            "name": f"Заказ #{order.pk}",
                        },
                        "unit_amount": int(order.total_cost * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=self.request.build_absolute_uri(reverse("orders:payment_success", kwargs={"pk": order.pk})),
            cancel_url=self.request.build_absolute_uri(reverse("orders:payment_cancel", kwargs={"pk": order.pk})),
            metadata={"order_id": order.pk},
            customer_email=order.customer.email,
        )

        order.stripe_session_id = session.id
        order.save(update_fields=["stripe_session_id"])

        return redirect(session.url)

    except stripe.error.StripeError:
        messages.error(self.request, "Произошла ошибка при обработке платежа. Пожалуйста, попробуйте еще раз.")
        return redirect("orders:checkout", order.pk)
