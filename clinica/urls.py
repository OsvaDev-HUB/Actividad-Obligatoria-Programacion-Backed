from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # La página de inicio es también el formulario de ingreso del personal
    path("", auth_views.LoginView.as_view(template_name="clinica/inicio.html", redirect_authenticated_user=True), name="inicio"),
    path("salir/", auth_views.LogoutView.as_view(), name="salir"),
    path("citas/", views.citas_dia, name="citas_dia"),
    path("citas/nueva/", views.agendar_cita, name="agendar_cita"),
    path("citas/<int:cita_id>/estado/", views.cambiar_estado, name="cambiar_estado"),
    path("pacientes/nuevo/", views.nuevo_paciente, name="nuevo_paciente"),
]
