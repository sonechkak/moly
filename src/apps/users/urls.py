from django.shortcuts import render
from django.urls import path

from .views import ProfileUpdateView, ProfileView

app_name = "users"

urlpatterns = [
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile-update"),
]
