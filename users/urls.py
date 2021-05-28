from django.urls import path, include
from users.views import DashboardView, Registrer

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    # Nos da acceso a multitud de url realacionadas con la gestión de usuario.
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", Registrer.as_view(), name="register"),


]