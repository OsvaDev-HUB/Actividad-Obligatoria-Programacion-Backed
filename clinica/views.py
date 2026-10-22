from datetime import time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .forms import CitaForm, MascotaForm
from .models import Cita, Mascota


def leer_fecha(texto):
    # Convierte "2026-10-22" en fecha; si viene vacía o mal escrita usa hoy
    try:
        fecha = parse_date(texto or "")
    except ValueError:
        fecha = None
    return fecha or timezone.localdate()


def bloques_de_atencion():
    # Horas de 09:00 a 18:30 cada 30 minutos
    return [time(hora, minuto) for hora in range(9, 19) for minuto in (0, 30)]


def horas_libres(cantidad_dias=2, maximo_por_dia=8):
    # Busca los próximos días que todavía tienen horas sin cita activa
    hoy = timezone.localdate()
    ahora = timezone.localtime().time()
    dias = []
    fecha = hoy
    while len(dias) < cantidad_dias and fecha <= hoy + timedelta(days=14):
        ocupadas = set(Cita.objects.filter(fecha=fecha).exclude(estado=Cita.CANCELADA).values_list("hora", flat=True))
        libres = [hora for hora in bloques_de_atencion() if hora not in ocupadas and (fecha > hoy or hora > ahora)]
        if libres:
            dias.append({
                "fecha": fecha,
                "es_hoy": fecha == hoy,
                "es_manana": fecha == hoy + timedelta(days=1),
                "horas": libres[:maximo_por_dia],
                "restantes": len(libres) - maximo_por_dia if len(libres) > maximo_por_dia else 0,
            })
        fecha += timedelta(days=1)
    return dias


def inicio(request):
    # Landing pública: solo muestra horarios libres, nunca datos de pacientes
    return render(request, "clinica/inicio.html", {"horas_libres": horas_libres()})


@login_required
def citas_dia(request):
    fecha = leer_fecha(request.GET.get("fecha"))
    hoy = timezone.localdate()
    citas = Cita.objects.filter(fecha=fecha).select_related("mascota")

    # Próxima cita pendiente: hoy desde la hora actual, o la primera de un día futuro
    siguiente = None
    pendientes = citas.filter(estado=Cita.PENDIENTE)
    if fecha == hoy:
        siguiente = pendientes.filter(hora__gte=timezone.localtime().time()).first()
    elif fecha > hoy:
        siguiente = pendientes.first()

    contexto = {
        "fecha": fecha,
        "hoy": hoy,
        "es_hoy": fecha == hoy,
        "dia_anterior": fecha - timedelta(days=1),
        "dia_siguiente": fecha + timedelta(days=1),
        "citas": citas,
        "siguiente": siguiente,
        "total_pendientes": pendientes.count(),
        "total_atendidas": citas.filter(estado=Cita.ATENDIDA).count(),
        "total_canceladas": citas.filter(estado=Cita.CANCELADA).count(),
    }
    return render(request, "clinica/citas_dia.html", contexto)


@login_required
def nuevo_paciente(request):
    form = MascotaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        mascota = form.save()
        messages.success(request, f"{mascota.nombre} quedó registrado. Ahora puedes agendar su primera cita.")
        return redirect(f"{reverse('agendar_cita')}?mascota={mascota.pk}")
    return render(request, "clinica/nuevo_paciente.html", {"form": form, "especies": Mascota.ESPECIES})


@login_required
def agendar_cita(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, f"Cita agendada: {cita.mascota.nombre}, {cita.fecha:%d-%m-%Y} a las {cita.hora:%H:%M}.")
            return redirect(f"{reverse('citas_dia')}?fecha={cita.fecha.isoformat()}")
    else:
        # Permite llegar con la mascota o la fecha ya elegidas
        inicial = {"fecha": leer_fecha(request.GET.get("fecha"))}
        if request.GET.get("mascota", "").isdigit():
            inicial["mascota"] = request.GET["mascota"]
        form = CitaForm(initial=inicial)
    return render(request, "clinica/agendar_cita.html", {"form": form})


@login_required
@require_POST
def cambiar_estado(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    nuevo_estado = request.POST.get("estado")
    # Desde recepción solo se cierra una cita pendiente
    if cita.estado == Cita.PENDIENTE and nuevo_estado in (Cita.ATENDIDA, Cita.CANCELADA):
        cita.estado = nuevo_estado
        cita.save()
        messages.success(request, f"La cita de {cita.mascota.nombre} quedó {cita.get_estado_display().lower()}.")
    return redirect(f"{reverse('citas_dia')}?fecha={cita.fecha.isoformat()}")
