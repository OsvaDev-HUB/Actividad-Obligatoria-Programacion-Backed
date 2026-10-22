# Prompts usados con el agente de IA

En este documento quedan las instrucciones (prompts) que se le dieron al agente de IA para acelerar el desarrollo. Cada prompt sigue la misma estructura: rol, contexto, tarea, requisitos y formato de la respuesta. Así el agente sabe para quién trabaja, qué tiene que entregar y cómo.

## Prompt 1: interfaz HTML/CSS del formulario de ingreso y de la tabla

```text
Rol: Eres un desarrollador frontend que trabaja con plantillas de Django.

Contexto: La clínica veterinaria "Huellas Sanas" atendía con agendas de papel y WhatsApp, y eso provocaba cruces de horario. Estamos construyendo un sistema en Django 5.2. Las recepcionistas lo usan en el computador del mesón de recepción. Ya existen los modelos:
- Mascota: nombre, especie (perro, gato, ave, conejo, roedor, reptil), raza, nombre_dueno.
- Cita: mascota (ForeignKey), fecha, hora, motivo, estado (pendiente, atendida, cancelada).

Tarea: Crea las plantillas HTML y una hoja de estilos CSS para:
1. Una página base con barra superior y menú: Citas del día, Nuevo paciente, Agendar cita y Salir.
2. Un formulario de ingreso de pacientes (MascotaForm) con nombre, especie, raza y nombre del dueño.
3. Una tabla con las citas del día con las columnas: hora, paciente, dueño, motivo y estado, más un selector para cambiar de día.

Requisitos:
- Diseño responsivo: en celular la tabla debe pasar a filas apiladas, sin scroll horizontal.
- Identidad visual basada en las placas de identificación de los collares: cada especie tiene el color de una placa y cada paciente aparece con una placa redonda con su inicial.
- El estado de la cita se muestra con un ícono y un texto, no solo con color.
- Mostrar los errores de cada campo del formulario y un mensaje cuando no hay citas ese día.
- Foco de teclado visible y contraste legible.
- Solo HTML, CSS y un poco de JavaScript simple, sin frameworks. Código fácil de entender, con comentarios cortos en español.

Formato de respuesta: Entrega cada archivo completo con su ruta (templates/clinica/... y static/clinica/...).
```

## Prompt 2: script con datos ficticios de 20 pacientes y sus citas

```text
Rol: Eres un desarrollador backend con experiencia en Django.

Contexto: En el proyecto Django de la clínica "Huellas Sanas" (app "clinica") existen los modelos Mascota y Cita. La cita tiene una restricción: no puede haber dos citas activas (no canceladas) en la misma fecha y hora. La clínica atiende de 09:00 a 18:30 en bloques de 30 minutos.

Tarea: Crea un comando de Django llamado "poblar_datos" (clinica/management/commands/poblar_datos.py) que genere datos ficticios para probar el sistema.

Requisitos:
- Crear 20 mascotas con nombres, especies, razas y dueños realistas para Chile.
- Crear una o dos citas por mascota, repartidas entre dos días atrás y cuatro días adelante, con varias citas para hoy.
- No repetir fecha y hora entre citas activas.
- Las citas que ya pasaron quedan atendidas o canceladas; las futuras quedan pendientes en su mayoría.
- Motivos de consulta realistas (vacunas, controles, desparasitación, etc.).
- Opción --borrar para limpiar los datos antes de crearlos.
- Crear un usuario "director" (superusuario) y un usuario "recepcion" para probar, solo si no existen.
- Usar solo la librería estándar de Python (random), sin instalar nada más.

Formato de respuesta: El archivo completo y el comando para ejecutarlo.
```

## Prompt 3: administrar las citas con el framework de Django

```text
Rol: Eres un desarrollador backend que conoce bien Django Admin y las vistas de Django.

Contexto: El director de la clínica "Huellas Sanas" necesita gestionar todo el sistema y las recepcionistas necesitan cerrar las citas del día. Las citas de prueba ya fueron generadas con el comando poblar_datos.

Tarea: Configura la administración de las citas usando solo el framework de Django.

Requisitos:
- Registrar Mascota y Cita en Django Admin con CRUD completo.
- En Cita: columnas fecha, hora, mascota, motivo y estado; filtros laterales por fecha y por estado; date_hierarchy por fecha; buscador por mascota, dueño y motivo; estado editable desde la lista.
- Acciones masivas: marcar como atendidas, canceladas o pendientes (al volver a pendiente, revisar que no choque con otra cita).
- En Mascota: ver sus citas dentro de la ficha (inline) y filtro por especie.
- En la agenda de recepción, agregar botones "Marcar atendida" y "Cancelar" para las citas pendientes, con una vista que solo acepte POST.
- Validar en el formulario de agendar cita que no se cruce con otra cita activa y mostrar un mensaje claro.

Formato de respuesta: Los archivos admin.py, views.py, urls.py y forms.py completos.
```

## Prompt extra: página de inicio con ingreso

```text
Rol: Eres un desarrollador Django.

Tarea: Agrega una página de inicio que presente el sistema de "Huellas Sanas" y tenga el formulario de ingreso del personal. Usa la LoginView de Django y protege las vistas de recepción con login_required. Si el usuario ya inició sesión, debe ir directo a la agenda del día. Mantén el mismo estilo de placas de identificación y que se vea bien en celular.
```
