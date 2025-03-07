from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.shop.models import Product


class Index(ListView):
    model = Product
    extra_context = {'title': 'Главная страница'}
    template_name = "shop/index.html"
