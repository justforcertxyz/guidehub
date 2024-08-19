from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Blog


class IndexListView(ListView):
    model = Blog
    template_name = "blog/index.html"


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/detail.html"
