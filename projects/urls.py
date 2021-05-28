from django.urls import path
from . import views

urlpatterns = [
    path("", views.Project_index.as_view(), name="project_index"),
    path("<int:pk>/", views.Project_Detail.as_view(), name="project_detail"),
]