from django.shortcuts import render
from django.views import generic
from .models import Project
# Create your views here.


class Project_index(generic.ListView):
    model = Project
    template_name = 'project_index.html'

class Project_Detail(generic.DetailView):
    model = Project
    template_name = 'project_detail.html'
