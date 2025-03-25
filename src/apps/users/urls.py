from django.urls import path
from django.shortcuts import render

from .views import ProfileView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
]
