from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Blog


class IndexListView(ListView):
    model = Blog
    template_name = "blog/index.html"
