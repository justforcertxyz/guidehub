from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Guide

class IndexListView(ListView):
    model = Guide
    template_name = "guide/index.html"