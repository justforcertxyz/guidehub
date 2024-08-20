from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Guide
from django.views.generic.detail import DetailView

class IndexListView(ListView):
    model = Guide
    template_name = "guide/index.html"

class GuideDetailView(DetailView):
    model = Guide
    template_name = "guide/detail.html"