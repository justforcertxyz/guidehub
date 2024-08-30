from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CreateInquiryForm
from django.urls import reverse_lazy


# TODO: Create success url
class CreateInquiryView(CreateView):
    template_name = 'contact/index.html'
    form_class = CreateInquiryForm
    success_url = reverse_lazy('landing:index')
