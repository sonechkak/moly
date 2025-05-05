from django.urls import path

from .views import ReferralLinkCreate, ReferralLinkView

app_name = "referral"


urlpatterns = [
    path("referral-link/<str:token>/", ReferralLinkView.as_view(), name="link"),
    path("referral/<int:pk>/create/", ReferralLinkCreate.as_view(), name="create"),
]
