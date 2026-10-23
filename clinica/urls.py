from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import IngresoForm

urlpatterns = [
    # Landing pública de la clínica
    path("", views.inicio, name="inicio"),
    # Ingreso del personal
    path("ingresar/", auth_views.LoginView.as_view(template_name="clinica/ingresar.html", authentication_form=IngresoForm, redirect_authenticated_user=True), name="ingresar"),
    path("salir/", auth_views.LogoutView.as_view(), name="salir"),
    path("citas/", views.citas_dia, name="citas_dia"),
    path("citas/nueva/", views.agendar_cita, name="agendar_cita"),
    path("citas/<int:cita_id>/estado/", views.cambiar_estado, name="cambiar_estado"),
    path("pacientes/nuevo/", views.nuevo_paciente, name="nuevo_paciente"),
]
