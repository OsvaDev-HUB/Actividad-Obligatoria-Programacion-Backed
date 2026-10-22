import random
from datetime import time, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from clinica.models import Cita, Mascota

# 20 pacientes ficticios: (nombre, especie, raza, dueño)
PACIENTES = [
    ("Rocky", "perro", "Quiltro", "Camila Rojas"),
    ("Misha", "gato", "Siamés", "Javier Muñoz"),
    ("Kiwi", "ave", "Catita australiana", "Fernanda Soto"),
    ("Luna", "perro", "Labrador", "Diego Fuentes"),
    ("Tomás", "gato", "Común europeo", "Valentina Díaz"),
    ("Copito", "conejo", "Cabeza de león", "Martina Herrera"),
    ("Bruno", "perro", "Pastor alemán", "Ignacio Vargas"),
    ("Pelusa", "gato", "Persa", "Antonia Castro"),
    ("Manchas", "perro", "Dálmata", "Sebastián Reyes"),
    ("Nala", "gato", "Bengalí", "Catalina Morales"),
    ("Pancho", "roedor", "Cuyi peruano", "Benjamín Silva"),
    ("Toby", "perro", "Beagle", "Josefa Pérez"),
    ("Simba", "gato", "Maine Coon", "Matías González"),
    ("Lola", "perro", "Poodle", "Isidora Contreras"),
    ("Pipo", "ave", "Canario", "Felipe Araya"),
    ("Tortuguita", "reptil", "Tortuga de tierra", "Sofía Espinoza"),
    ("Max", "perro", "Golden retriever", "Tomás Sepúlveda"),
    ("Canela", "conejo", "Belier", "Florencia Tapia"),
    ("Chispa", "roedor", "Hámster sirio", "Vicente Navarro"),
    ("Olivia", "gato", "Quiltro", "Paula Riquelme"),
]

MOTIVOS = [
    "Vacuna antirrábica anual",
    "Control de rutina",
    "Desparasitación interna y externa",
    "Vómitos desde ayer",
    "Cojea de la pata trasera derecha",
    "Control post operatorio",
    "Revisión de piel por picazón",
    "Limpieza dental",
    "Corte de uñas",
    "No quiere comer hace dos días",
    "Vacuna séxtuple",
    "Esterilización: evaluación previa",
    "Ojo irritado y lagrimeo",
    "Control de peso",
]

# Días respecto de hoy donde caen las citas (hoy aparece más veces para tener una agenda llena)
DIAS = [-2, -1, 0, 0, 0, 0, 0, 1, 1, 2, 3, 4]

# Usuarios de prueba: (usuario, contraseña, es director)
USUARIOS = [
    ("director", "DirectorHuellas2026!", True),
    ("recepcion", "RecepcionHuellas2026!", False),
]


def horas_de_atencion():
    # Bloques de 30 minutos entre las 09:00 y las 18:30
    return [time(hora, minuto) for hora in range(9, 19) for minuto in (0, 30)]


class Command(BaseCommand):
    help = "Crea 20 pacientes ficticios con sus citas y los usuarios de prueba"

    def add_arguments(self, parser):
        parser.add_argument("--borrar", action="store_true", help="Borra mascotas y citas antes de crear los datos")

    def handle(self, *args, **options):
        if options["borrar"]:
            Cita.objects.all().delete()
            Mascota.objects.all().delete()
            self.stdout.write("Se borraron las mascotas y citas anteriores.")

        self.crear_usuarios()

        hoy = timezone.localdate()
        ahora = timezone.localtime().time()
        # Horarios ya ocupados, para no generar cruces
        ocupados = set(Cita.objects.exclude(estado=Cita.CANCELADA).values_list("fecha", "hora"))
        total_citas = 0

        for nombre, especie, raza, dueno in PACIENTES:
            mascota = Mascota.objects.create(nombre=nombre, especie=especie, raza=raza, nombre_dueno=dueno)

            # Cada paciente tiene una o dos citas
            for _ in range(random.choice([1, 1, 2])):
                fecha, hora = self.buscar_horario_libre(hoy, ocupados)
                estado = self.elegir_estado(fecha, hora, hoy, ahora)
                Cita.objects.create(mascota=mascota, fecha=fecha, hora=hora, motivo=random.choice(MOTIVOS), estado=estado)
                if estado != Cita.CANCELADA:
                    ocupados.add((fecha, hora))
                total_citas += 1

        self.stdout.write(self.style.SUCCESS(f"Listo: {len(PACIENTES)} pacientes y {total_citas} citas creadas."))

    def buscar_horario_libre(self, hoy, ocupados):
        while True:
            fecha = hoy + timedelta(days=random.choice(DIAS))
            hora = random.choice(horas_de_atencion())
            if (fecha, hora) not in ocupados:
                return fecha, hora

    def elegir_estado(self, fecha, hora, hoy, ahora):
        # Las citas que ya pasaron quedan atendidas o canceladas; las futuras, en su mayoría pendientes
        ya_paso = fecha < hoy or (fecha == hoy and hora < ahora)
        if ya_paso:
            return random.choice([Cita.ATENDIDA, Cita.ATENDIDA, Cita.ATENDIDA, Cita.CANCELADA])
        return random.choice([Cita.PENDIENTE] * 6 + [Cita.CANCELADA])

    def crear_usuarios(self):
        for usuario, clave, es_director in USUARIOS:
            if User.objects.filter(username=usuario).exists():
                continue
            if es_director:
                User.objects.create_superuser(username=usuario, password=clave)
            else:
                User.objects.create_user(username=usuario, password=clave)
            self.stdout.write(f"Usuario creado: {usuario}")
