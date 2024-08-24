from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterUserForm
from django.views.generic.edit import CreateView
from guide.models import Guide


class IndexView(TemplateView):
    template_name = "landing/index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "landing/privacy_policy.html"


class ImprintView(TemplateView):
    template_name = "landing/imprint.html"


class LoginUserView(LoginView):
    template_name = "landing/login.html"
    next_page = reverse_lazy("landing:index")


class LogoutUserView(LoginRequiredMixin, LogoutView):
    http_method_names = ["get", "post"]
    template_name = "landing/logout.html"
    next_page = reverse_lazy("landing:index")
    login_url = "landing:login"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterUserView(CreateView):
    template_name = "landing/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("landing:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "landing/dashboard.html"
    login_url = "landing:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["guides_owned"] = [guide for guide in Guide.objects.all().order_by('current_price')[:3] if guide.is_owned(self.request.user)]
        context["guides_written"] = [guide for guide in Guide.objects.all().order_by('current_price')[:3] if guide.author == self.request.user]
        return context
    
