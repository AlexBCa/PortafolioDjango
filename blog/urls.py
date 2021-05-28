from django.urls import path
from . import views

urlpatterns = [
    path("", views.BlogIndex.as_view(), name="blog_index"),
    path("<int:pk>/", views.BlogView.as_view(), name="blog_detail"),
    path("<category>/", views.BlogCategory.as_view(), name="blog_category"),
    path("secret/private/", views.ViewPrivada.as_view(), name="private"),
    path("secret/staff/", views.ViewStaff.as_view(), name="staff"),
]