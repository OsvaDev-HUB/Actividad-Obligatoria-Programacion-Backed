# Huellas Sanas: agenda de la clínica veterinaria

Actividad Obligatoria 2 de Programación Back End (INACAP).

La clínica veterinaria "Huellas Sanas" manejaba sus citas con agendas de papel y mensajes de WhatsApp, y eso causaba cruces de horario y pérdida de los motivos de consulta. Este proyecto es un sistema web en Django para registrar a los pacientes y sus citas en un solo lugar.

## Qué incluye

- **Modelos con ORM** (`clinica/models.py`): `Mascota` (nombre, especie, raza, nombre del dueño) y `Cita` (mascota, fecha, hora, motivo de consulta y estado pendiente/atendida/cancelada). Una restricción impide dos citas activas en la misma fecha y hora.
- **Django Admin** (`clinica/admin.py`): CRUD completo de mascotas y citas, con filtros por fecha y estado, búsqueda, estado editable desde la lista y acciones para marcar varias citas como atendidas, canceladas o pendientes.
- **Vistas y rutas** (`clinica/views.py`, `clinica/urls.py`):
  - `/`: landing pública de la clínica para los dueños de mascotas, con las próximas horas libres tomadas de la agenda y un aviso cuando quedan pocas.
  - `/ingresar/`: ingreso del personal, con mensajes de error por campo, botón para mostrar la contraseña y aviso de Bloq Mayús.
  - `/citas/`: citas del día, con la próxima cita arriba, las horas libres del día (cada una lleva a agendar con la hora puesta), cambio de día y botones para marcar una cita como atendida o cancelarla.
  - `/pacientes/nuevo/`: ingreso de pacientes nuevos, con una ficha de la mascota que se arma en vivo.
  - `/citas/nueva/`: agendar una cita sin cruces de horario. Las horas ocupadas y las que ya pasaron quedan deshabilitadas, y al lado se ven las horas libres del día elegido.
  - `/admin/`: panel del director.
- **Datos de prueba** (`clinica/management/commands/poblar_datos.py`): genera 20 pacientes ficticios con sus citas y los usuarios de prueba.
- **Uso de IA**: los prompts usados están en [`docs/prompts_ia.md`](docs/prompts_ia.md).

## Instalación

Se necesita Python 3.

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py poblar_datos
python manage.py runserver
```

En Windows:

```bash
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py poblar_datos
python manage.py runserver
```

Luego se abre <http://127.0.0.1:8000/>. El personal entra con el botón «Ingreso del personal» de la barra de arriba o en <http://127.0.0.1:8000/ingresar/>. Para volver a generar los datos desde cero se usa `python manage.py poblar_datos --borrar`.

## Usuarios de prueba

El comando `poblar_datos` los crea si no existen.

| Rol | Usuario | Contraseña | Dónde ingresa |
| --- | --- | --- | --- |
| Director (superusuario) | `director` | `DirectorHuellas2026!` | <http://127.0.0.1:8000/admin/> |
| Recepcionista | `recepcion` | `RecepcionHuellas2026!` | <http://127.0.0.1:8000/ingresar/> |

El teléfono y la dirección de la landing son datos de ejemplo.

Las imágenes de mascotas son propias de la clínica; solo la foto de la sección de contacto es de dominio público (CC0). El origen de cada una está en `clinica/static/clinica/img/CREDITOS.md`.

## Tecnologías

- Python 3 y Django 5.2
- SQLite
- HTML, CSS y JavaScript simple (sin frameworks)
