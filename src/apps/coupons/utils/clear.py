def clear_coupons_session(request):
    """Очищает сессию после применения купона."""
    del request.session["coupon_code"]
    del request.session["coupon_id"]
    del request.session["coupon_discount"]
