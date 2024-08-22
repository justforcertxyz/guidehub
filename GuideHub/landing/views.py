from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = "landing/index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "landing/privacy_policy.html"


class ImprintView(TemplateView):
    template_name = "landing/imprint.html"


class LoginUserView(LoginView):
    template_name = "landing/login.html"
    next_page = reverse_lazy("landing:index")
