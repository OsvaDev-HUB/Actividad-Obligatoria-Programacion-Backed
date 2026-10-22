from django.db import models
from django.db.models import Q


class Mascota(models.Model):
    # Especies que atiende la clínica (valor guardado, texto que se muestra)
    ESPECIES = [
        ("perro", "Perro"),
        ("gato", "Gato"),
        ("ave", "Ave"),
        ("conejo", "Conejo"),
        ("roedor", "Roedor"),
        ("reptil", "Reptil"),
    ]

    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raza = models.CharField(max_length=50)
    nombre_dueno = models.CharField("nombre del dueño", max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()}) - {self.nombre_dueno}"


class Cita(models.Model):
    PENDIENTE = "pendiente"
    ATENDIDA = "atendida"
    CANCELADA = "cancelada"
    ESTADOS = [
        (PENDIENTE, "Pendiente"),
        (ATENDIDA, "Atendida"),
        (CANCELADA, "Cancelada"),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="citas")
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField("motivo de consulta", max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PENDIENTE)

    class Meta:
        ordering = ["fecha", "hora"]
        constraints = [
            # Evita los cruces de horario: no puede haber dos citas activas
            # en la misma fecha y hora (las canceladas liberan el horario)
            models.UniqueConstraint(
                fields=["fecha", "hora"],
                condition=~Q(estado="cancelada"),
                name="cita_unica_por_horario",
                violation_error_message="Ya hay una cita agendada en esa fecha y hora. Elige otro horario.",
            ),
        ]

    def __str__(self):
        return f"{self.fecha:%d-%m-%Y} {self.hora:%H:%M} - {self.mascota.nombre}"
