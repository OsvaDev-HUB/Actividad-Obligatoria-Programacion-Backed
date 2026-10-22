from datetime import time

from django import forms
from django.utils import timezone

from .models import Cita, Mascota


def horas_de_atencion():
    # Bloques de 30 minutos entre las 09:00 y las 18:30
    horas = []
    for hora in range(9, 19):
        for minuto in (0, 30):
            texto = f"{hora:02d}:{minuto:02d}"
            horas.append((texto, texto))
    return horas


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["nombre", "especie", "raza", "nombre_dueno"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Rocky", "autocomplete": "off"}),
            "especie": forms.RadioSelect,
            "raza": forms.TextInput(attrs={"placeholder": "Ej: Quiltro, Labrador, Siamés"}),
            "nombre_dueno": forms.TextInput(attrs={"placeholder": "Ej: Camila Rojas", "autocomplete": "off"}),
        }
        labels = {
            "nombre": "Nombre de la mascota",
        }


class CitaForm(forms.ModelForm):
    hora = forms.TimeField(widget=forms.Select(choices=horas_de_atencion()))

    class Meta:
        model = Cita
        fields = ["mascota", "fecha", "hora", "motivo"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "motivo": forms.Textarea(attrs={"rows": 3, "placeholder": "Ej: Vacuna antirrábica, control post operatorio"}),
        }
        labels = {
            "mascota": "Paciente",
        }

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha < timezone.localdate():
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data["hora"]
        if not (time(9, 0) <= hora <= time(18, 30)):
            raise forms.ValidationError("Elige una hora entre las 09:00 y las 18:30.")
        return hora

    def clean(self):
        datos = super().clean()
        fecha = datos.get("fecha")
        hora = datos.get("hora")
        # Revisa que no exista otra cita activa (no cancelada) en la misma fecha y hora
        if fecha and hora:
            ocupada = Cita.objects.filter(fecha=fecha, hora=hora).exclude(estado=Cita.CANCELADA).exists()
            if ocupada:
                raise forms.ValidationError("Ya hay una cita agendada en esa fecha y hora. Elige otro horario.")
        return datos
