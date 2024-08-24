from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic.list import ListView
from .models import Guide
from django.views.generic.detail import DetailView
from django.http import FileResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexListView(ListView):
    model = Guide
    template_name = "guide/index.html"


class GuideDetailView(DetailView):
    model = Guide
    template_name = "guide/detail.html"


def download_view(request, *args, **kwargs):
    guide = get_object_or_404(Guide, slug=kwargs['slug'])

    if guide.is_owned(request.user):
        return FileResponse(guide.guide_pdf.open(), as_attachment=True)
    else:
        # TODO: Create not owned page
        return HttpResponseRedirect(reverse('landing:index'))