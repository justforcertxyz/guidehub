from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("datenschutz", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("impressum/", views.ImprintView.as_view(), name="imprint"),
    path("anmelden/", views.LoginUserView.as_view(), name="login"),
    path("abmelden", views.LogoutUserView.as_view(), name="logout"),
    path("registrieren/", views.RegisterUserView.as_view(), name="register"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]