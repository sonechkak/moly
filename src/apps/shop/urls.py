from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="shop/index.html"), name="index"),
]
