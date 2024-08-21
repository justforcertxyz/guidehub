from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("datenschutz", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("impressum/", views.ImprintView.as_view(), name="imprint"),
]