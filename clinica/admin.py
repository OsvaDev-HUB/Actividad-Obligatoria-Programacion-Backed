from django.contrib import admin
from .models import Cita, Mascota

# Textos del encabezado del panel de administración
admin.site.site_header = "Huellas Sanas - Administración"
admin.site.site_title = "Huellas Sanas"
admin.site.index_title = "Gestión de la clínica"


class CitaInline(admin.TabularInline):
    # Muestra las citas de la mascota dentro de su ficha
    model = Cita
    extra = 0


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "raza", "nombre_dueno")
    search_fields = ("nombre", "raza", "nombre_dueno")
    list_filter = ("especie",)
    inlines = [CitaInline]


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "mascota", "motivo", "estado")
    # Filtros laterales por fecha y estado que pide el director
    list_filter = ("fecha", "estado")
    # Navegación por año, mes y día sobre la lista
    date_hierarchy = "fecha"
    # Permite cambiar el estado directo desde la lista
    list_editable = ("estado",)
    search_fields = ("mascota__nombre", "mascota__nombre_dueno", "motivo")
    autocomplete_fields = ("mascota",)
    actions = ["marcar_atendida", "marcar_cancelada", "marcar_pendiente"]

    @admin.action(description="Marcar como atendidas")
    def marcar_atendida(self, request, queryset):
        cantidad = queryset.update(estado=Cita.ATENDIDA)
        self.message_user(request, f"{cantidad} cita(s) marcadas como atendidas.")

    @admin.action(description="Marcar como canceladas")
    def marcar_cancelada(self, request, queryset):
        cantidad = queryset.update(estado=Cita.CANCELADA)
        self.message_user(request, f"{cantidad} cita(s) marcadas como canceladas.")

    @admin.action(description="Marcar como pendientes")
    def marcar_pendiente(self, request, queryset):
        # Al volver a pendiente se revisa una por una que no choque con otra cita activa
        cambiadas = 0
        for cita in queryset.exclude(estado=Cita.PENDIENTE):
            choca = Cita.objects.filter(fecha=cita.fecha, hora=cita.hora).exclude(estado=Cita.CANCELADA).exclude(pk=cita.pk).exists()
            if not choca:
                cita.estado = Cita.PENDIENTE
                cita.save()
                cambiadas += 1
        self.message_user(request, f"{cambiadas} cita(s) marcadas como pendientes.")
