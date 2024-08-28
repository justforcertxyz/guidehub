from django.urls import path
from . import views

app_name = "guide"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("<slug:slug>/download", views.download_view, name="download"),
    path("<slug:slug>", views.GuideDetailView.as_view(), name="detail"),
]
