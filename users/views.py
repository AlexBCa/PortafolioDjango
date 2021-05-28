from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from users.form import CustomUserCreationForm
from django.urls import reverse

# Create your views here.

class DashboardView(TemplateView):
    template_name = 'users/dashboard.html'

class Registrer(CreateView):

    template_name = 'users/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('dashboard')
